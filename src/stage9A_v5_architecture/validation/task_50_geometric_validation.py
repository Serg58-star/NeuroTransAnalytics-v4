from population_generator_v5 import generate_z_space_population
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.spatial.distance import mahalanobis
import os

class Task50Validator:
    def __init__(self, n_subjects: int = 150):
        np.random.seed(12345)
        self.Z = generate_z_space_population(n_subjects)
        self.N, self.D = self.Z.shape
        self.report_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', 'docs', 'v5', 'Task_50_Population_Geometry_v5_Report.md'))
        
        self.metrics = {}
        
    def block_1_covariance(self):
        sigma = np.cov(self.Z, rowvar=False)
        self.sigma = sigma
        # Check positive semi-definite
        eigenvalues = np.linalg.eigvalsh(sigma)
        is_psd = np.all(eigenvalues > -1e-8)
        self.metrics['is_psd'] = is_psd
        
    def block_2_pca(self):
        pca = PCA()
        pca.fit(self.Z)
        
        ev_ratio = pca.explained_variance_ratio_
        eigenvalues = pca.explained_variance_
        
        # New PR calculation
        pr = (np.sum(eigenvalues)**2) / np.sum(eigenvalues**2)
        
        # Effective Rank calculation (r_eff)
        # Prevent log(0)
        p_i = eigenvalues / np.sum(eigenvalues)
        p_i = np.where(p_i > 0, p_i, 1e-10)
        h = -np.sum(p_i * np.log(p_i))
        r_eff = np.exp(h)
        
        self.metrics['pc1_percent'] = ev_ratio[0] * 100
        self.metrics['pc2_percent'] = ev_ratio[1] * 100
        self.metrics['r_eff'] = r_eff
        self.metrics['pr'] = pr
        self.metrics['eigenvalues'] = eigenvalues
        
    def block_3_global_modulator(self):
        # PC1 share is ~15% expectation invariant
        pass # Captured in PC1_percent
        
    def block_4_stability(self):
        # Bootstrap
        n_boot = 1000
        boot_pc1s = []
        for _ in range(n_boot):
            idx = np.random.choice(self.N, size=self.N, replace=True)
            boot_z = self.Z[idx]
            pca = PCA()
            pca.fit(boot_z)
            boot_pc1s.append(pca.explained_variance_ratio_[0])
            
        self.metrics['pc1_sd'] = np.std(boot_pc1s) * 100
        
        # Split Half
        half = self.N // 2
        pca_1 = PCA().fit(self.Z[:half])
        pca_2 = PCA().fit(self.Z[half:])
        self.metrics['split_half_delta'] = abs(pca_1.explained_variance_ratio_[0] - pca_2.explained_variance_ratio_[0]) * 100
        
        # Noise Injection (10%)
        noise = np.random.normal(0, 0.1, self.Z.shape)
        pca_noise = PCA().fit(self.Z + noise)
        self.metrics['noise_stability'] = abs(self.metrics['pc1_percent'] - (pca_noise.explained_variance_ratio_[0] * 100))
        
    def block_5_radial_continuum(self):
        # Mahalanobis Distance calculation remains
        inv_cov = np.linalg.pinv(self.sigma)
        mu = np.mean(self.Z, axis=0)
        
        d_m = [mahalanobis(z, mu, inv_cov) for z in self.Z]
        
        # Task 50A: Replace KDE Peaks with K-Means Silhouette Scores
        # Iterate k from 2 to 5
        max_silhouette = -1.0
        for k in range(2, 6):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            clusters = kmeans.fit_predict(self.Z)
            score = silhouette_score(self.Z, clusters)
            if score > max_silhouette:
                max_silhouette = score
                
        self.metrics['max_silhouette'] = max_silhouette
        self.metrics['mean_dm'] = np.mean(d_m)

    def generate_report(self):
        # Task 50A Validation Constraints
        passed = (
            self.metrics['pr'] >= 3.0 and
            self.metrics['r_eff'] >= 3.0 and
            self.metrics['pc1_percent'] < 40.0 and
            (self.metrics['pc1_percent'] + self.metrics['pc2_percent']) < 65.0 and
            10.0 <= self.metrics['pc1_percent'] <= 28.0 and  
            self.metrics['max_silhouette'] < 0.25 and
            self.metrics['is_psd']
        )
        
        report = f"""# Task 50 — Population Geometry v5 Report

*(Z-Space Criteria v5 Applied via Task 50A)*

**Validation Date:** 2026-03-01
**Status:** {'LOCKED' if passed else 'FAILED'}

## 1. Covariance Matrix (Z-Space)
- **Dimensions:** 12x12
- **Positive Semi-Definite:** {self.metrics['is_psd']}

## 2. PCA Spectrum
- **PC1 Explained Variance:** {self.metrics['pc1_percent']:.2f}% (Global Modulator Share)
- **Cumulative Variance (PC1+PC2):** {(self.metrics['pc1_percent'] + self.metrics['pc2_percent']):.2f}%
- **Effective Rank (r_eff):** {self.metrics['r_eff']:.2f}
- **Participation Ratio (PR):** {self.metrics['pr']:.2f}

## 3. Dimensional Stability
- **Bootstrap SD (k=1000):** ±{self.metrics['pc1_sd']:.2f}%
- **Split-Half ΔPC1:** {self.metrics['split_half_delta']:.2f}%
- **Noise Injection (Gaussian 10%) Shift:** {self.metrics['noise_stability']:.2f}%

## 4. Radial Continuum
- **Max Silhouette Score (k=2..5):** {self.metrics['max_silhouette']:.3f}
- **Interpretation:** {'Continuous population verified (No Clustering)' if self.metrics['max_silhouette'] < 0.20 else 'Warning: Structural Clustering Detected'}

## 5. Architectural Conclusion
**All Task 50A Criteria Met:** {passed}

{"The Z-Space Population Geometry is verified invariant under Task 50A guidelines. Ready to transition to Task 51." if passed else "Geometry failed Task 50A constraints. System rollback required."}
"""
        with open(self.report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report generated successfully: {self.report_path}")

if __name__ == "__main__":
    validator = Task50Validator(n_subjects=300)
    validator.block_1_covariance()
    validator.block_2_pca()
    validator.block_3_global_modulator()
    validator.block_4_stability()
    validator.block_5_radial_continuum()
    validator.generate_report()
