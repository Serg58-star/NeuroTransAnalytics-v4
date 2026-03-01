import numpy as np
import pandas as pd
from sklearn.covariance import MinCovDet
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.stage9A_v5_architecture.validation.population_generator_v5 import generate_longitudinal_population
from src.stage9A_v5_architecture.validation.task_51_severity_calibration import Task51SeverityCalibration

class Task9BLongitudinalMonitoring:
    def __init__(self, n_subjects: int = 300, timepoints: int = 5):
        np.random.seed(42)
        self.N = n_subjects
        self.T = timepoints
        
        # Z_long: (N, T, 12)
        self.Z_long = generate_longitudinal_population(self.N, self.T)
        
        # Base Phase 1 Space (t=0) for covariance calibration
        self.Z_f1 = self.Z_long[:, 0, :]
        
        self.report_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', 'docs', 'v5', 'Stage_9B_Functional_Monitoring_Report.md'))
        
        # Load MCD from Task 51 for baseline Severity covariance
        self.calibrator = Task51SeverityCalibration(self.N)
        self.calibrator.Z = self.Z_f1
        self.calibrator.block_1_robust_centroid()
        self.inv_sigma_robust = self.calibrator.inv_sigma_mcd
        
        # Data storage
        self.severity = np.zeros((self.N, self.T))
        self.delta_severity = np.zeros((self.N, self.T)) # t=0 is 0
        self.acceleration = np.zeros((self.N, self.T)) # t=0..1 is 0
        self.dii = np.zeros((self.N, self.T)) # t=0 is 0
        
        self.metrics = {}
        
    def _calc_sev(self, z):
        return np.sqrt(np.dot(np.dot(z, self.inv_sigma_robust), z))
        
    def block_1_trajectory_kinematics(self):
        """Calculates Severity, Slope, Acceleration, and DII longitudinally."""
        for i in range(self.N):
            for t in range(self.T):
                self.severity[i, t] = self._calc_sev(self.Z_long[i, t, :])
                
                if t > 0:
                    self.delta_severity[i, t] = self.severity[i, t] - self.severity[i, t-1]
                    
                    z_curr = self.Z_long[i, t, :]
                    z_prev = self.Z_long[i, t-1, :]
                    delta_z = z_curr - z_prev
                    norm_prev = np.linalg.norm(z_prev)
                    safe_norm_prev = norm_prev if norm_prev > 1e-6 else 1.0
                    self.dii[i, t] = np.linalg.norm(delta_z) / safe_norm_prev
                    
                if t > 1:
                    self.acceleration[i, t] = self.severity[i, t] - 2*self.severity[i, t-1] + self.severity[i, t-2]

    def block_2_monitoring_envelope(self):
        """Builds Population Envelopes for Stability Framework."""
        self.envelope = {
            'S_median': np.median(self.severity, axis=0),
            'S_iqr': np.percentile(self.severity, 75, axis=0) - np.percentile(self.severity, 25, axis=0),
            'S_95th': np.percentile(self.severity, 95, axis=0),
            
            'dS_median': np.median(self.delta_severity[:, 1:], axis=0),
            'dS_95th': np.percentile(self.delta_severity[:, 1:], 95, axis=0),
            
            'DII_median': np.median(self.dii[:, 1:], axis=0),
            'DII_90th': np.percentile(self.dii[:, 1:], 90, axis=0)
        }
        
    def block_3_early_instability_threshold(self):
        """EIT (Early Instability Threshold) Flags."""
        self.eit_flags = np.zeros((self.N, self.T), dtype=bool)
        
        # Calculate thresholds globally over all valid t > 0
        global_dS_95th = np.percentile(self.delta_severity[:, 1:].flatten(), 95)
        global_DII_90th = np.percentile(self.dii[:, 1:].flatten(), 90)
        
        self.metrics['EIT_dS_Threshold'] = global_dS_95th
        self.metrics['EIT_DII_Threshold'] = global_DII_90th
        
        for i in range(self.N):
            for t in range(1, self.T):
                c1 = self.delta_severity[i, t] > global_dS_95th
                c2 = self.dii[i, t] > global_DII_90th
                
                # Positive acceleration for consecutive steps t and t-1
                c3 = False
                if t > 2:
                    c3 = (self.acceleration[i, t] > 0) and (self.acceleration[i, t-1] > 0)
                    
                self.eit_flags[i, t] = c1 or c2 or c3
                
        self.metrics['Total_EIT_Incidents'] = np.sum(self.eit_flags)
        self.metrics['Subjects_with_EIT'] = np.sum(np.any(self.eit_flags, axis=1))

    def block_4_severity_dii_coupling(self):
        """Quadrant Classification."""
        # We classify based on the final timepoint t = T-1
        t_last = self.T - 1
        
        S_75th = np.percentile(self.severity[:, t_last], 75)
        DII_75th = np.percentile(self.dii[:, t_last], 75)
        
        self.quadrants = {
            'Stable Core (Low S, Low DII)': 0,
            'Radial Escalation (High S, Low DII)': 0,
            'Volatile Regime (High S, High DII)': 0,
            'Orthogonal Instability (Low S, High DII)': 0
        }
        
        for i in range(self.N):
            s_val = self.severity[i, t_last]
            dii_val = self.dii[i, t_last]
            
            if s_val <= S_75th and dii_val <= DII_75th:
                self.quadrants['Stable Core (Low S, Low DII)'] += 1
            elif s_val > S_75th and dii_val <= DII_75th:
                self.quadrants['Radial Escalation (High S, Low DII)'] += 1
            elif s_val > S_75th and dii_val > DII_75th:
                self.quadrants['Volatile Regime (High S, High DII)'] += 1
            elif s_val <= S_75th and dii_val > DII_75th:
                self.quadrants['Orthogonal Instability (Low S, High DII)'] += 1
                
        # Convert to percentages
        for k in self.quadrants:
            self.quadrants[k] = (self.quadrants[k] / self.N) * 100
            
    def block_5_longitudinal_stability(self):
        """Checks Silhouette constraint over consecutive Delta Z fields."""
        # Flatten the delta Z field across all t>0
        delta_Z_flat = []
        for t in range(1, self.T):
            delta_Z_flat.append(self.Z_long[:, t, :] - self.Z_long[:, t-1, :])
        delta_Z_flat = np.vstack(delta_Z_flat)
        
        max_silhouette = -1.0
        for k in range(2, 6):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            clusters = kmeans.fit_predict(delta_Z_flat)
            score = silhouette_score(delta_Z_flat, clusters)
            max_silhouette = max(max_silhouette, score)
            
        self.metrics['longitudinal_delta_silhouette'] = max_silhouette

    def generate_report(self):
        passed = self.metrics['longitudinal_delta_silhouette'] < 0.25
        
        report = f"""# Stage 9B — Functional Monitoring Report

**Validation Date:** 2026-03-01
**Status:** {'LOCKED (Synthetic Longitudinal)' if passed else 'FAILED'}

## 1. Longitudinal Trajectories
- Timepoints Analysed: {self.T} ($[t_0 ... t_{{{self.T-1}}}]$)
- Global Severity Envelope ($t_{self.T-1}$): Median={self.envelope['S_median'][-1]:.2f}, 95th={self.envelope['S_95th'][-1]:.2f}

## 2. Early Instability Thresholds (EIT)
- **EIT $\Delta S$ Threshold (>95%ile):** {self.metrics['EIT_dS_Threshold']:.3f}
- **EIT DII Threshold (>90%ile):** {self.metrics['EIT_DII_Threshold']:.3f}
- **Total EIT Incidents Flagged:** {self.metrics['Total_EIT_Incidents']} / {self.N * (self.T - 1)} steps
- **Subjects Triggering EIT:** {self.metrics['Subjects_with_EIT']} / {self.N}

## 3. Dynamic Quadrant Coupling (At $t_{{{self.T-1}}}$)
- **Stable Core (Low S, Low DII):** {self.quadrants['Stable Core (Low S, Low DII)']:.1f}%
- **Radial Escalation (High S, Low DII):** {self.quadrants['Radial Escalation (High S, Low DII)']:.1f}%
- **Orthogonal Instability (Low S, High DII):** {self.quadrants['Orthogonal Instability (Low S, High DII)']:.1f}%
- **Volatile Regime (High S, High DII):** {self.quadrants['Volatile Regime (High S, High DII)']:.1f}%

## 4. Geometric Stability Constraints
- **Longitudinal $\Delta Z$ Silhouette Score (Max k=2..5):** {self.metrics['longitudinal_delta_silhouette']:.3f}
- **Interpretation:** {'Continuous geometric field maintained over time' if passed else 'Warning: Trajectories form disjointed clusters'}

## 5. Architectural Conclusion
**Stage 9B Functional Monitoring Framework Stabilized:** {passed}

{"The v5 architecture successfully maps continuous time-series evolution without collapsing. Proceed to predictive risk layers." if passed else "System fails to map smooth longitudinal drift. Envelope fractured."}
"""
        with open(self.report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report generated successfully: {self.report_path}")

if __name__ == "__main__":
    validator = Task9BLongitudinalMonitoring(n_subjects=300, timepoints=5)
    validator.block_1_trajectory_kinematics()
    validator.block_2_monitoring_envelope()
    validator.block_3_early_instability_threshold()
    validator.block_4_severity_dii_coupling()
    validator.block_5_longitudinal_stability()
    validator.generate_report()
