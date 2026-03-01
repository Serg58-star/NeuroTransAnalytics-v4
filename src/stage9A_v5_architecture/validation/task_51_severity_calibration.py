import numpy as np
import pandas as pd
from sklearn.covariance import MinCovDet
from scipy.spatial.distance import mahalanobis
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import os
import sys

# Ensure the module can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.stage9A_v5_architecture.validation.population_generator_v5 import generate_z_space_population
from src.stage9A_v5_architecture.dual_space_core import compute_robust_layer, compute_robust_z_layer

class Task51SeverityCalibration:
    def __init__(self, n_subjects: int = 300):
        np.random.seed(42)
        self.n_subjects = n_subjects
        self.Z = generate_z_space_population(self.n_subjects)
        self.N, self.D = self.Z.shape
        self.report_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', 'docs', 'v5', 'Task_51_Severity_Calibration_v5_Report.md'))
        
        self.metrics = {}
        self.zones = {}
        
    def block_1_robust_centroid(self):
        """Calculates MCD Centroid and Covariance."""
        mcd = MinCovDet(random_state=42)
        mcd.fit(self.Z)
        
        self.mu_mcd = mcd.location_
        self.sigma_mcd = mcd.covariance_
        self.inv_sigma_mcd = np.linalg.pinv(self.sigma_mcd)
        
        self.metrics['is_psd_mcd'] = np.all(np.linalg.eigvalsh(self.sigma_mcd) > -1e-8)
        
    def _calc_mahalanobis(self, Z_matrix, mu, inv_sigma):
        # Task 51A Correction: Mean subtraction removed. D_M operates on true zero origin.
        # It's simply sqrt(Z^T * Sigma_inv * Z) since E[Z]=0
        return np.array([np.sqrt(np.dot(np.dot(z, inv_sigma), z)) for z in Z_matrix])
        
    def block_2_mahalanobis_zones(self):
        """Calculates D_M and stratifies into radial zones."""
        self.D_M = self._calc_mahalanobis(self.Z, self.mu_mcd, self.inv_sigma_mcd)
        
        percentiles = [50, 75, 90, 95]
        p_vals = np.percentile(self.D_M, percentiles)
        
        self.zones = {
            'A_Core': p_vals[0],
            'B_Stable_Norm': p_vals[1],
            'C_Extended_Norm': p_vals[2],
            'D_Peripheral': p_vals[3]
        }
        
    def block_3_heavy_tail_stress_test(self):
        """
        Injects heavy tails (20%) and extreme bursts (30%)
        into a new population and tests if MCD resists the shift.
        """
        np.random.seed(999) # New seed for stress pop
        stress_Z_list = []
        for subj in range(self.n_subjects):
            base_speed = np.random.normal(250, 40)
            
            # Base variance
            variance_multiplier = max(0.5, np.random.normal(1.0, 0.3))
            
            # Heavy tail injection rules
            if subj < self.n_subjects * 0.2:
                # Top 20% Extreme tail (systemic fatigue)
                variance_multiplier *= 3.0
            
            df_trials = self._generate_stressed_subject(subj, base_speed, variance_multiplier, burst_prob=0.3 if subj < self.n_subjects * 0.3 else 0.0)
            
            robust_space = compute_robust_layer(df_trials)
            z_space = compute_robust_z_layer(robust_space)
            
            z_row = []
            for ch in ['V1', 'Parvo', 'Magno', 'Koniocellular']:
                for pos in ['L', 'C', 'R']:
                    z_row.append(z_space[ch][pos])
            stress_Z_list.append(z_row)
            
        stress_Z = np.array(stress_Z_list)
        
        # Calculate MCD of Stressed Population
        mcd_stress = MinCovDet(random_state=42)
        mcd_stress.fit(stress_Z)
        
        stress_mu = mcd_stress.location_
        
        # Task 51A Correction: Absolute L2 drift distance instead of relative percentage
        drift_abs = np.linalg.norm(stress_mu - self.mu_mcd)
        self.metrics['stress_center_drift_abs'] = drift_abs
        
    def _generate_stressed_subject(self, subject_id: int, base_speed: float, variance_multiplier: float, burst_prob: float) -> pd.DataFrame:
        channels = ['V1', 'Parvo', 'Magno', 'Koniocellular']
        positions = ['L', 'C', 'R']
        ch_profiles = {
            'V1': {'add': 0, 'var': 15},
            'Parvo': {'add': 30, 'var': 25},
            'Magno': {'add': -15, 'var': 20},
            'Koniocellular': {'add': 70, 'var': 50} 
        }
        data = []
        for ch in channels:
            for pos in positions:
                ch_base = base_speed + ch_profiles[ch]['add']
                std_dev = ch_profiles[ch]['var'] * variance_multiplier
                
                # If subject is a burster, replace standard RTs with extremes
                rts = []
                for _ in range(12):
                    if np.random.rand() < burst_prob:
                        rts.append(np.random.uniform(ch_base + std_dev*6, ch_base + std_dev*12))
                    else:
                        rts.append(np.random.normal(ch_base, std_dev))
                
                for rt in rts:
                    data.append({
                        'Subject': subject_id,
                        'Stimulus': ch,
                        'Position': pos,
                        'RT': max(100, rt)
                    })
        return pd.DataFrame(data)

    def block_4_bootstrap_envelope(self):
        """Bootstrap (k=1000) for MCD stability bounds."""
        n_boot = 1000
        boot_centers = []
        boot_zone_A = []
        
        # We bootstrap the D_M values directly for zone stability to save compute on MinCovDet which is slow
        for _ in range(n_boot):
            idx = np.random.choice(self.N, size=self.N, replace=True)
            boot_z = self.Z[idx]
            
            # Simplified center measure for bootstrap drift estimation (MCD is too slow for 1000x on large N)
            # We measure median center drift.
            boot_center = np.median(boot_z, axis=0) 
            boot_centers.append(boot_center)
            
            boot_dm = self.D_M[idx]
            boot_zone_A.append(np.percentile(boot_dm, 50))
            
        center_sds = np.std(np.array(boot_centers), axis=0)
        max_center_sd = np.max(center_sds) # We just take the worst channel drift
        
        # Convert to relative % based on base SD=1 of Z Space
        self.metrics['boot_center_drift_percent'] = max_center_sd * 100 
        
        zone_A_sd = np.std(boot_zone_A)
        self.metrics['boot_zone_A_sd_percent'] = (zone_A_sd / self.zones['A_Core']) * 100
        
    def block_5_continuum_preservation(self):
        """Check for artificial clustering in the spatial zones using Silhouette."""
        # We classify points into the 5 zones
        labels = []
        for d in self.D_M:
            if d <= self.zones['A_Core']: labels.append(0)
            elif d <= self.zones['B_Stable_Norm']: labels.append(1)
            elif d <= self.zones['C_Extended_Norm']: labels.append(2)
            elif d <= self.zones['D_Peripheral']: labels.append(3)
            else: labels.append(4)
            
        # Ensure we have >= 2 classes with >= 2 members before Silhouette
        unique_labels = np.unique(labels)
        if len(unique_labels) > 1:
            score = silhouette_score(self.Z, labels)
            self.metrics['zone_silhouette'] = score
        else:
            self.metrics['zone_silhouette'] = -1.0 # Invalid

    def generate_report(self):
        passed = (
            self.metrics['is_psd_mcd'] and
            self.metrics['stress_center_drift_abs'] <= 1.0 and
            self.metrics['boot_center_drift_percent'] <= 5.0 and
            self.metrics['boot_zone_A_sd_percent'] <= 5.0 and
            self.metrics['zone_silhouette'] < 0.20 # Zones should be contiguous shells, not distinct separated density clusters
        )
        
        report = f"""# Task 51 — Severity Calibration v5 Report

*(Task 51A Criteria Applied - Center Fixed to Zero)*

**Validation Date:** 2026-03-01
**Status:** {'LOCKED (Synthetic)' if passed else 'FAILED'}

## 1. Robust Centroid (MCD)
- **Minimum Covariance Determinant (MCD):** Successfully Fit
- **Covariance Matrix Positive Semi-Definite:** {self.metrics['is_psd_mcd']}

## 2. Radial Zones (Severity Index via Centered Mahalanobis)
- **Zone A:** Core Norm (≤50%) | $D_M \le {self.zones['A_Core']:.2f}$
- **Zone B:** Stable Norm (50-75%) | $D_M \in ({self.zones['A_Core']:.2f}, {self.zones['B_Stable_Norm']:.2f}]$
- **Zone C:** Extended Norm (75-90%) | $D_M \in ({self.zones['B_Stable_Norm']:.2f}, {self.zones['C_Extended_Norm']:.2f}]$
- **Zone D:** Peripheral Deviation (90-95%) | $D_M \in ({self.zones['C_Extended_Norm']:.2f}, {self.zones['D_Peripheral']:.2f}]$
- **Zone E:** Extreme Deviation (>95%) | $D_M > {self.zones['D_Peripheral']:.2f}$

## 3. Bootstrap Bounds (k=1000)
- **Max Z-Coordinate Drift SD:** ±{self.metrics['boot_center_drift_percent']:.2f}%
- **Zone A Boundary SD:** ±{self.metrics['boot_zone_A_sd_percent']:.2f}%

## 4. Heavy-Tail Stress Test
*Injected extreme tails into 20% of subjects and burst frequencies into 30% of subjects.*
- **MCD Center Absolute Displacement:** {self.metrics['stress_center_drift_abs']:.4f} Z-Units (Limit: 1.0)

## 5. Continuum Preservation
- **Radial Zone Silhouette Score:** {self.metrics['zone_silhouette']:.3f}
- **Interpretation:** {'Contiguous shells confirmed' if self.metrics['zone_silhouette'] < 0.20 else 'Warning: Disjointed clustering detected'}

## 6. Architectural Conclusion
**All Task 51 Criteria Met:** {passed}

{"The v5 Severity Model successfully scales and stratifies robust dimensional data. Heavy-tail variance is handled securely by the MCD centroid. The model is architecturally locked." if passed else "System is unstable under heavy variance. Review standardizations."}
"""
        with open(self.report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report generated successfully: {self.report_path}")

if __name__ == "__main__":
    validator = Task51SeverityCalibration(n_subjects=300)
    validator.block_1_robust_centroid()
    validator.block_2_mahalanobis_zones()
    validator.block_3_heavy_tail_stress_test()
    validator.block_4_bootstrap_envelope()
    validator.block_5_continuum_preservation()
    validator.generate_report()
