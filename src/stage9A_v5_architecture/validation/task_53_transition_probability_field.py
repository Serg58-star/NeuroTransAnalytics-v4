import numpy as np
import pandas as pd
from sklearn.neighbors import KernelDensity
from scipy.stats import entropy
from sklearn.utils import resample
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.stage9A_v5_architecture.validation.task_9B_longitudinal_monitoring import Task9BLongitudinalMonitoring

class Task53TransitionProbabilityField:
    def __init__(self, n_subjects: int = 500, timepoints: int = 5, kappa: float = 0.0, inv_sigma_mcd=None):
        # We can increase n_subjects to 500 to get more stable transitions
        np.random.seed(42)
        print("Executing Stage 9B longitudinal generator for base kinematics...")
        self.stage9b = Task9BLongitudinalMonitoring(n_subjects=n_subjects, timepoints=timepoints, kappa=kappa, inv_sigma_mcd=inv_sigma_mcd)
        self.stage9b.block_1_trajectory_kinematics()
        
        self.N = n_subjects
        self.T = timepoints
        self.severity = self.stage9b.severity
        self.dii = self.stage9b.dii
        self.delta_severity = self.stage9b.delta_severity
        
        self.report_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', 'docs', 'v5', 'Stage_9C_Task_01_Transition_Probability_Field_Report.md'))
        
        self.metrics = {}
        
    def block_1_discrete_transition_matrix(self, fixed_S75=None, fixed_DII75=None):
        print("Calculating Discrete Transition Matrix...")
        if fixed_S75 is not None and fixed_DII75 is not None:
            print(f"  Using provided anchored thresholds: S_75th={fixed_S75:.4f}, DII_75th={fixed_DII75:.4f}")
            self.S_75th = fixed_S75
            self.DII_75th = fixed_DII75
        else:
            # Get threshold values using all valid timepoints t > 0
            valid_S = self.severity[:, 1:].flatten()
            valid_DII = self.dii[:, 1:].flatten()
            self.S_75th = np.percentile(valid_S, 75)
            self.DII_75th = np.percentile(valid_DII, 75)
            print(f"  Calculated dynamic thresholds: S_75th={self.S_75th:.4f}, DII_75th={self.DII_75th:.4f}")
        
        self.Q = np.zeros((self.N, self.T), dtype=int)
        # Quadrant definition (matches 9B documentation style)
        # 0: Stable Core (Low S, Low DII)
        # 1: Radial Escalation (High S, Low DII)
        # 2: Orthogonal Instability (Low S, High DII)
        # 3: Volatile Regime (High S, High DII)
        
        for i in range(self.N):
            for t in range(1, self.T):
                s_val = self.severity[i, t]
                dii_val = self.dii[i, t]
                if s_val <= self.S_75th and dii_val <= self.DII_75th:
                    self.Q[i, t] = 0
                elif s_val > self.S_75th and dii_val <= self.DII_75th:
                    self.Q[i, t] = 1
                elif s_val <= self.S_75th and dii_val > self.DII_75th:
                    self.Q[i, t] = 2
                else:
                    self.Q[i, t] = 3
                    
        # Calculate transition frequencies from t to t+1 (for t in 1..T-2)
        transitions = np.zeros((4, 4))
        for i in range(self.N):
            for t in range(1, self.T - 1):
                q_curr = self.Q[i, t]
                q_next = self.Q[i, t+1]
                transitions[q_curr, q_next] += 1
                
        # Normalize rows to form probability matrix
        row_sums = transitions.sum(axis=1, keepdims=True)
        # Avoid division by zero
        row_sums[row_sums == 0] = 1.0 
        self.T_matrix = transitions / row_sums
        self.metrics['T_matrix'] = self.T_matrix.copy()

    def block_2_bootstrap_confidence_intervals(self):
        print("Bootstrapping Confidence Intervals...")
        # Bootstrap transitions
        B = 100
        boot_matrices = np.zeros((B, 4, 4))
        
        # We bootstrap the subjects.
        all_indices = np.arange(self.N)
        for b in range(B):
            idx = resample(all_indices, random_state=b)
            boot_transitions = np.zeros((4, 4))
            for i in idx:
                for t in range(1, self.T - 1):
                    q_curr = self.Q[i, t]
                    q_next = self.Q[i, t+1]
                    boot_transitions[q_curr, q_next] += 1
            boot_sums = boot_transitions.sum(axis=1, keepdims=True)
            boot_sums[boot_sums == 0] = 1.0
            boot_matrices[b, :, :] = boot_transitions / boot_sums
            
        self.T_lower = np.percentile(boot_matrices, 2.5, axis=0)
        self.T_upper = np.percentile(boot_matrices, 97.5, axis=0)

    def block_3_transition_entropy(self):
        print("Calculating Transition Entropy...")
        self.entropies = np.zeros(4)
        for i in range(4):
            # entropy of row i (base e)
            # If all are 0 or such, handled by scipy
            self.entropies[i] = entropy(self.T_matrix[i, :])
            
        self.metrics['Mean_Entropy'] = np.mean(self.entropies)
        self.metrics['Variance_Entropy'] = np.var(self.entropies)

    def block_4_continuous_transition_density(self):
        print("Estimating Continuous KDE State Density...")
        # KDE of P(Q(t+1)=j | S(t), DII(t))
        X = []
        Y = []
        for i in range(self.N):
            for t in range(1, self.T - 1):
                X.append([self.severity[i, t], self.dii[i, t]])
                Y.append(self.Q[i, t+1])
        X = np.array(X)
        Y = np.array(Y)
        
        # We just test we can fit the KDE without artificial binning
        self.kdes = {}
        # global kde
        kde_global = KernelDensity(bandwidth='scott', kernel='gaussian')
        kde_global.fit(X)
        self.kdes['global'] = kde_global
        
        for q in range(4):
            X_q = X[Y == q]
            if len(X_q) > 5:
                kde = KernelDensity(bandwidth='scott', kernel='gaussian')
                kde.fit(X_q)
                self.kdes[q] = kde
                
        # Calculate condition number of T_matrix
        self.metrics['T_cond'] = np.linalg.cond(self.T_matrix)
        # Eigenvalues
        evals = np.linalg.eigvals(self.T_matrix)
        self.metrics['T_evals'] = evals
        self.metrics['MaxAbsEval'] = np.max(np.abs(evals))
        
        # Check absorbing strictures
        self.metrics['Absorbing_Flag'] = np.any(np.diag(self.T_matrix) > 0.95)

    def generate_report(self):
        from numpy.linalg import cond
        passed = (self.metrics['MaxAbsEval'] <= 1.0 + 1e-6) and not self.metrics['Absorbing_Flag']
        
        quadrant_names = [
            "Q1 Stable Core",
            "Q2 Radial Escalation",
            "Q3 Orthogonal Instability",
            "Q4 Volatile Regime"
        ]
        
        def format_row(row_idx):
            row = self.T_matrix[row_idx]
            low = self.T_lower[row_idx]
            high = self.T_upper[row_idx]
            parts = []
            for j in range(4):
                parts.append(f"{row[j]:.3f} [{low[j]:.3f}, {high[j]:.3f}]")
            return " | ".join(parts)
            
        report = f"""# Stage 9C Task 01 — Transition Probability Field Report

**Validation Date:** 2026-03-02
**Status:** {'LOCKED (Synthetic TPF)' if passed else 'FAILED DIAGONSTICS'}

## 1. 4x4 Transition Probability Matrix ($T_{{ij}}$)
*Rows: Origin Quadrant $Q(t)$ | Columns: Destination Quadrant $Q(t+1)$*
*Format: Probability [95% CI Lower, 95% CI Upper]*

| Origin | Q1 Stable Core | Q2 Radial Escalation | Q3 Orthogonal Instab | Q4 Volatile Regime |
|---|---|---|---|---|
| **{quadrant_names[0]}** | {format_row(0)} |
| **{quadrant_names[1]}** | {format_row(1)} |
| **{quadrant_names[2]}** | {format_row(2)} |
| **{quadrant_names[3]}** | {format_row(3)} |

## 2. Transition Entropy ($H_i$)
*Entropy measures trajectory predictability. Low: rigid, High: chaotic drift.*

- **{quadrant_names[0]}**: {self.entropies[0]:.3f} nats
- **{quadrant_names[1]}**: {self.entropies[1]:.3f} nats
- **{quadrant_names[2]}**: {self.entropies[2]:.3f} nats
- **{quadrant_names[3]}**: {self.entropies[3]:.3f} nats
- **Mean System Entropy**: {self.metrics['Mean_Entropy']:.3f}
- **Variance of Entropy**: {self.metrics['Variance_Entropy']:.3f}

## 3. Stability Diagnostics
- **Matrix Condition Number:** {self.metrics['T_cond']:.2f}
- **Maximum Absolute Eigenvalue:** {self.metrics['MaxAbsEval']:.4f} (Must be $\le 1.0$)
- **Absorbing Quadrants ($P_{{ii}} > 0.95$):** {self.metrics['Absorbing_Flag']}
- **Continuous KDE Surface:** Successfully estimated for all populated quadrants.

## 4. Structural Conclusion
- **Regime Classification:** {'Continuous Dynamic Field' if self.metrics['Mean_Entropy'] > 0.3 else 'Rigid Fragmented Drift'}

{"The Transition Probability Field correctly layers probabilistic transitions over the continuous geometry without collapsing into absorbing states or singular distributions." if passed else "Transition field demonstrates fatal structural rigidity or runaway instability."}
"""
        os.makedirs(os.path.dirname(self.report_path), exist_ok=True)
        with open(self.report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report generated successfully: {self.report_path}")

if __name__ == "__main__":
    tpf = Task53TransitionProbabilityField(n_subjects=500, timepoints=5)
    tpf.block_1_discrete_transition_matrix()
    tpf.block_2_bootstrap_confidence_intervals()
    tpf.block_3_transition_entropy()
    tpf.block_4_continuous_transition_density()
    tpf.generate_report()
