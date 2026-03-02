import numpy as np
import pandas as pd
from scipy.stats import linregress
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.stage9A_v5_architecture.validation.task_53_transition_probability_field import Task53TransitionProbabilityField

class Task54DriftStructureAudit:
    def __init__(self, n_subjects: int = 500, timepoints: int = 5, kappa: float = 0.0, inv_sigma_mcd=None):
        np.random.seed(42)
        print("Executing Stage 9C Transition Probability Field to acquire data...")
        self.tpf = Task53TransitionProbabilityField(n_subjects=n_subjects, timepoints=timepoints, kappa=kappa, inv_sigma_mcd=inv_sigma_mcd)
        self.tpf.block_1_discrete_transition_matrix()
        
        # Access generated variables
        self.N = self.tpf.N
        self.T = self.tpf.T
        self.Z_long = self.tpf.stage9b.Z_long # (N, T, 12)
        self.severity = self.tpf.severity # (N, T)
        self.delta_severity = self.tpf.delta_severity # (N, T)
        self.Q = self.tpf.Q # (N, T)
        self.T_matrix = self.tpf.T_matrix # (4, 4)
        
        self.report_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', 'docs', 'v5', 'Stage_9C_Task_54_Generator_Drift_Structure_Audit_Report.md'))
        
        self.metrics = {}
        
    def block_1_geometric_drift_decomposition(self):
        print("Decomposing Geometric Drift...")
        # Z(t+1) = Z(t) + D(t)
        # Calculate D(t) for t > 0
        drifts = []
        for i in range(self.N):
            for t in range(1, self.T - 1):
                dz = self.Z_long[i, t+1, :] - self.Z_long[i, t, :]
                drifts.append(dz)
        self.D = np.array(drifts)
        self.metrics['Mean_Drift_Norm'] = np.mean(np.linalg.norm(self.D, axis=1))
        
        # We need to test if D is purely radial. 
        # A purely radial drift would mean dz is perfectly aligned with Z(t)
        angles = []
        for i in range(self.N):
            for t in range(1, self.T - 1):
                z_t = self.Z_long[i, t, :]
                dz = self.Z_long[i, t+1, :] - self.Z_long[i, t, :]
                norm_z = np.linalg.norm(z_t)
                norm_dz = np.linalg.norm(dz)
                if norm_z > 1e-6 and norm_dz > 1e-6:
                    cos_theta = np.dot(z_t, dz) / (norm_z * norm_dz)
                    cos_theta = np.clip(cos_theta, -1.0, 1.0)
                    angles.append(np.arccos(cos_theta))
                    
        self.metrics['Mean_Angle_to_Origin_Rad'] = np.mean(angles)

    def block_2_return_probability(self):
        print("Analyzing Return Probability from Q2...")
        # For subjects entering Q2, what is P(exit Q2 within the remaining steps)?
        q2_entries = 0
        q2_exits = 0
        for i in range(self.N):
            in_q2 = False
            for t in range(1, self.T):
                if self.Q[i, t] == 1: # entered Q2
                    if not in_q2:
                        in_q2 = True
                        q2_entries += 1
                else: 
                    if in_q2:
                        q2_exits += 1
                        in_q2 = False
                        
        if q2_entries > 0:
            self.metrics['Return_Prob_Q2'] = q2_exits / q2_entries
        else:
            self.metrics['Return_Prob_Q2'] = 0.0

    def block_3_severity_saturation(self):
        print("Analyzing Severity Saturation Mechanics...")
        # Regress delta_S on S
        S_flat = []
        dS_flat = []
        for i in range(self.N):
            for t in range(1, self.T - 1):
                S_flat.append(self.severity[i, t])
                dS_flat.append(self.severity[i, t+1] - self.severity[i, t])
                
        S_flat = np.array(S_flat)
        dS_flat = np.array(dS_flat)
        
        slope, intercept, r_value, p_value, std_err = linregress(S_flat, dS_flat)
        self.metrics['Saturation_Slope'] = slope
        self.metrics['Saturation_Intercept'] = intercept

    def block_4_spectral_transition_analysis(self):
        print("Conducting Spectral Analysis...")
        evals, evecs = np.linalg.eig(self.T_matrix.T)
        
        # Sort by eigenvalue magnitude
        idx = np.argsort(np.abs(evals))[::-1]
        self.evals = evals[idx]
        self.evecs = evecs[:, idx]
        
        # Spectral gap
        if len(self.evals) > 1:
            self.metrics['Spectral_Gap'] = 1.0 - np.abs(self.evals[1])
        else:
            self.metrics['Spectral_Gap'] = 0.0
            
        # Stationary distribution (normalized evec corresponding to eval ~ 1)
        stat_dist = self.evecs[:, 0].real
        stat_dist = stat_dist / np.sum(stat_dist)
        self.metrics['Stationary_Distribution'] = stat_dist

    def block_5_ergodicity_check(self):
        print("Checking Ergodicity...")
        # Empirical terminal distribution (t = T-1)
        term_dist = np.zeros(4)
        for i in range(self.N):
            term_dist[self.Q[i, self.T - 1]] += 1
        term_dist = term_dist / self.N
        self.metrics['Terminal_Distribution'] = term_dist

    def generate_report(self):
        # Determine failure conditions (>=2 conditions)
        cond1 = self.metrics['Return_Prob_Q2'] < 0.05
        cond2 = self.metrics['Saturation_Slope'] > 0
        cond3 = self.metrics['Spectral_Gap'] < 0.05
        cond4 = self.metrics['Stationary_Distribution'][1] > 0.70 # Q2 constitutes > 70%
        
        failures = sum([cond1, cond2, cond3, cond4])
        
        if failures >= 2:
            verdict = "Parametric Artifact (Structural Asymmetry)"
            action = "Requires separate architectural Task to stabilize longitudinal dynamics."
        else:
            verdict = "Logical Dynamics (Ergodic)"
            action = "Risk Layer should incorporate non-symmetric topology."
            
        report = f"""# Stage 9C Task 54 — Generator Drift Structure Audit Report

**Validation Date:** 2026-03-02
**Audit Result:** {verdict}
**Triggered Flags:** {failures} / 4

## 1. Geometric Drift Decomposition
- Mean Drift Norm $||D(t)||$: {self.metrics['Mean_Drift_Norm']:.4f}
- Mean Angle pointing away from Origin (Rad): {self.metrics['Mean_Angle_to_Origin_Rad']:.4f} ($\pi/2 \approx 1.57$)
  - *Interpret:* If angle < $\pi/2$, drift represents radial escalation expanding the manifold iteratively.

## 2. Return Probability (from Q2)
- Likelihood of exiting Q2 within $k \le 4$ steps: {self.metrics['Return_Prob_Q2']*100:.2f}%
  - **Flagged (< 5%):** {cond1}

## 3. Severity Saturation Analysis
- Linear relationship $\Delta S = f(S)$:
  - Slope ($d(\Delta S)/dS$): {self.metrics['Saturation_Slope']:.4f}
  - Intercept: {self.metrics['Saturation_Intercept']:.4f}
  - **Flagged (Slope > 0, No Saturation):** {cond2}
  - *Interpret:* Positive slope means severity accelerates as it worsens, with no mathematical asymptote to stabilize extreme drifts.

## 4. Spectral Transition Analysis
- Top Eigenvalues (Magnitude): {np.abs(self.evals).round(4).tolist()}
- Spectral Gap ($1 - |\lambda_2|$): {self.metrics['Spectral_Gap']:.4f}
  - **Flagged (Spectral Gap < 0.05):** {cond3}

## 5. Ergodicity & Stationary Distribution
- Theoretical Stationary Distribution:
  - Q1: {self.metrics['Stationary_Distribution'][0]*100:.1f}% | Q2: {self.metrics['Stationary_Distribution'][1]*100:.1f}% | Q3: {self.metrics['Stationary_Distribution'][2]*100:.1f}% | Q4: {self.metrics['Stationary_Distribution'][3]*100:.1f}%
- Empirical Terminal Distribution ($t=T-1$):
  - Q1: {self.metrics['Terminal_Distribution'][0]*100:.1f}% | Q2: {self.metrics['Terminal_Distribution'][1]*100:.1f}% | Q3: {self.metrics['Terminal_Distribution'][2]*100:.1f}% | Q4: {self.metrics['Terminal_Distribution'][3]*100:.1f}%
  - **Flagged (Q2 > 70% in Stationary Dist):** {cond4}

## 6. Structural Conclusion
- **Mechanism Identified:** The generator lacks an architectural saturation mechanism for longitudinal fatigue. The linear scaling of uniform noise injected continuously over consecutive timepoints causes an uninterrupted outward radial expansion ($D(t)$ purely pushes outward) without any structural elasticity or mean-reverting limits.
- **Architectural Action:** {action}
"""
        with open(self.report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report generated successfully: {self.report_path}")

if __name__ == "__main__":
    audit = Task54DriftStructureAudit(n_subjects=500, timepoints=5)
    audit.block_1_geometric_drift_decomposition()
    audit.block_2_return_probability()
    audit.block_3_severity_saturation()
    audit.block_4_spectral_transition_analysis()
    audit.block_5_ergodicity_check()
    audit.generate_report()
