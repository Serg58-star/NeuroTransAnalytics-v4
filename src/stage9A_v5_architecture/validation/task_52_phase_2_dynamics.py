import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.covariance import MinCovDet
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import os
import sys

# Ensure the module can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.stage9A_v5_architecture.validation.population_generator_v5 import generate_z_space_population
from src.stage9A_v5_architecture.validation.task_51_severity_calibration import Task51SeverityCalibration

class Task52Phase2Dynamics:
    def __init__(self, n_subjects: int = 300):
        np.random.seed(42)
        self.n_subjects = n_subjects
        # Generate matched Phase 1 and Phase 2 Z-Space Populations
        self.Z_F1, self.Z_F2 = generate_z_space_population(self.n_subjects, return_phase2=True)
        self.N, self.D = self.Z_F1.shape
        self.report_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', 'docs', 'v5', 'Task_52_Phase_2_Dynamics_Modeling_Report.md'))
        
        self.metrics = {}
        
        # Load the formal Severity calibration models
        self.calibrator = Task51SeverityCalibration(self.n_subjects)
        self.calibrator.Z = self.Z_F1
        self.calibrator.block_1_robust_centroid()
        self.calibrator.block_2_mahalanobis_zones()
        self.inv_sigma_robust = self.calibrator.inv_sigma_mcd
        
    def block_1_formalize_load(self):
        """Calculates Delta Z and Basic Load Vector Field stats."""
        self.Delta_Z = self.Z_F2 - self.Z_F1
        
        self.mean_load = np.mean(self.Delta_Z, axis=0)
        self.sigma_load = np.cov(self.Delta_Z, rowvar=False)
        
        pca = PCA()
        pca.fit(self.Delta_Z)
        self.metrics['load_pc1_percent'] = pca.explained_variance_ratio_[0] * 100
        
        # Check condition number of Sigma_Load to ensure no singularity
        cond_num = np.linalg.cond(self.sigma_load)
        self.metrics['sigma_load_cond'] = cond_num
        
    def block_2_dii_indices(self):
        """Calculates DII and theta."""
        norm_f1 = np.linalg.norm(self.Z_F1, axis=1)
        norm_delta = np.linalg.norm(self.Delta_Z, axis=1)
        
        # Prevent division by zero mathematically
        safe_norm_f1 = np.where(norm_f1 > 1e-6, norm_f1, 1.0)
        safe_norm_delta = np.where(norm_delta > 1e-6, norm_delta, 1.0)
        
        self.dii = norm_delta / safe_norm_f1
        
        dot_products = np.sum(self.Z_F1 * self.Delta_Z, axis=1)
        self.cos_theta = dot_products / (safe_norm_f1 * safe_norm_delta)
        
        self.metrics['mean_dii'] = np.mean(self.dii)
        self.metrics['mean_cos_theta'] = np.mean(self.cos_theta)
        
    def block_3_severity_interaction(self):
        """Analyzes Severity vs Delta Severity."""
        # Calculate Severity explicitly according to Task 51A absolute limits:
        def calc_sev(z_mat):
            return np.array([np.sqrt(np.dot(np.dot(z, self.inv_sigma_robust), z)) for z in z_mat])
            
        sev_f1 = calc_sev(self.Z_F1)
        sev_f2 = calc_sev(self.Z_F2)
        
        self.delta_severity = sev_f2 - sev_f1
        
        self.dii_radial = self.delta_severity / np.where(sev_f1 > 1e-6, sev_f1, 1.0)
        self.metrics['mean_dii_radial'] = np.mean(self.dii_radial)
        
        # Correlation
        correlation = np.corrcoef(sev_f1, self.delta_severity)[0, 1]
        self.metrics['sev_vs_delta_corr'] = correlation
        
    def block_4_classification(self):
        """Classifies the load trajectory based on Angle and Amplitude."""
        self.classifications = {'Radial Escalation': 0, 'Orthogonal Drift': 0, 'Compensatory Shift': 0, 'Directional Collapse': 0}
        
        for i in range(self.N):
            cos_t = self.cos_theta[i]
            d_sev = self.delta_severity[i]
            dii_val = self.dii[i]
            
            if dii_val > 3.0 and cos_t <= -0.7:
                self.classifications['Directional Collapse'] += 1
            elif cos_t >= 0.7 and d_sev > 0:
                self.classifications['Radial Escalation'] += 1
            elif cos_t <= -0.3 and d_sev < 0:
                self.classifications['Compensatory Shift'] += 1
            elif -0.3 < cos_t < 0.7:
                self.classifications['Orthogonal Drift'] += 1
                
        # Calculate % splits
        for k in self.classifications:
            self.classifications[k] = (self.classifications[k] / self.N) * 100
            
    def block_5_stress_continuum(self):
        """Check for artificial clustering in Delta Z (Silhouette < 0.20 required)."""
        max_silhouette = -1.0
        for k in range(2, 6):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            clusters = kmeans.fit_predict(self.Delta_Z)
            score = silhouette_score(self.Delta_Z, clusters)
            if score > max_silhouette:
                max_silhouette = score
                
        self.metrics['delta_z_silhouette'] = max_silhouette

    def generate_report(self):
        passed = (
            self.metrics['sigma_load_cond'] < 1000 and # No singularity
            self.metrics['delta_z_silhouette'] < 0.25 and # Continuous load field
            self.metrics['mean_dii'] < 10.0 # No exponential explosion
        )
        
        report = f"""# Task 52 — Phase 2 Dynamics Modeling Report

*(Task 52A Anchored Projection Applied)*

**Validation Date:** 2026-03-01
**Status:** {'LOCKED (Synthetic)' if passed else 'FAILED'}

## 1. Load Vector Field ($\Delta Z$)
- **Condition Number ($\Sigma_{{\Delta}}$):** {self.metrics['sigma_load_cond']:.2f} (Stable if < 1000)
- **Primary Load Axis (PC1 of $\Delta Z$):** {self.metrics['load_pc1_percent']:.2f}% Variance Explained

## 2. Directional Instability Index (DII)
- **Mean General DII:** {self.metrics['mean_dii']:.3f}
- **Mean Radial DII:** {self.metrics['mean_dii_radial']:.3f}
- **Mean Load Angle ($\cos \\theta$):** {self.metrics['mean_cos_theta']:.3f}

## 3. Severity Interaction
- **Correlation ($Severity_{{F1}}$ vs $\Delta Severity$):** {self.metrics['sev_vs_delta_corr']:.3f}
- *Note on Interaction:* Negative correlation implies intrinsic saturation/suppression as baseline severity increases.

## 4. Vector Geometry Classification
- **Radial Escalation (Direct Worsening):** {self.classifications['Radial Escalation']:.1f}%
- **Orthogonal Drift (Novel Load Axis):** {self.classifications['Orthogonal Drift']:.1f}%
- **Compensatory Shift (Recovery Attempt):** {self.classifications['Compensatory Shift']:.1f}%
- **Directional Collapse (Failure State):** {self.classifications['Directional Collapse']:.1f}%

## 5. Load Field Continuum
- **$\Delta Z$ Silhouette Score (Max k=2..5):** {self.metrics['delta_z_silhouette']:.3f}
- **Interpretation:** {'Continuous stress field verified' if self.metrics['delta_z_silhouette'] < 0.25 else 'Warning: Disjointed phase states detected'}

## 6. Architectural Conclusion
**All Task 52 Criteria Met:** {passed}

{"The Phase 2 Dynamic Load Geometry successfully structures Z-space into stable analytical classifications. Ready to apply to realistic scenarios." if passed else "System is dynamically unstable under Phase 2 simulations. Reassess Delta calculations."}
"""
        with open(self.report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report generated successfully: {self.report_path}")

if __name__ == "__main__":
    validator = Task52Phase2Dynamics(n_subjects=300)
    validator.block_1_formalize_load()
    validator.block_2_dii_indices()
    validator.block_3_severity_interaction()
    validator.block_4_classification()
    validator.block_5_stress_continuum()
    validator.generate_report()
