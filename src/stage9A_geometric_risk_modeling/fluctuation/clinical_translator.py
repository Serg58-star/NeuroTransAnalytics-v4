"""
stage9A_geometric_risk_modeling.fluctuation.clinical_translator

Implements the dictionary lookup masking internal mathematical mechanics 
(standard deviations, orthogonal matrices, coordinate names) into pure 
clinically-approved terminology based on consecutive significance thresholds.
"""

import pandas as pd

class ClinicalTranslator:
    def __init__(self, significance_threshold: float = 1.96, k_min_consecutive: int = 2):
        """
        Args:
            significance_threshold: Absolute Z-score cutoff.
            k_min_consecutive: Number of consecutive outliers required to trigger stable clinical shift.
        """
        self.threshold = significance_threshold
        self.k_min_consecutive = k_min_consecutive

    def translate_speed(self, k_z_s: int, z_s: float) -> str:
        """ Speed translation rules """
        if k_z_s >= self.k_min_consecutive:
            return "Statistically significant change detected."
        elif abs(z_s) > self.threshold:
            return "Transient deviation observed. Monitor for persistence."
        return "Reaction speed remains within expected physiological variability."
        
    def translate_lateralization(self, k_z_l: int, z_l: float) -> str:
        """ Lateralization / Synchrony rules """
        if k_z_l >= self.k_min_consecutive:
            return "Statistically significant change detected."
        elif abs(z_l) > self.threshold:
            return "Transient deviation observed. Monitor for persistence."
        return "No statistically significant change in hemispheric balance."
        
    def translate_tone(self, k_z_t: int, z_t: float) -> str:
        """ Residual Tone rules """
        if k_z_t >= self.k_min_consecutive:
            return "Statistically significant change detected."
        elif abs(z_t) > self.threshold:
            return "Transient deviation observed. Monitor for persistence."
        return "Tone remains stable at the individual baseline level."

    def translate_global_state(self, k_z_r: int, k_z_m: int, z_r: float, z_m: float, z_cum: float, vol_r: int, vol_m: int) -> str:
        """ Cumulative geometric trajectory rules (Masks 'Cumulative Radial Drift' logic and Volatility) """
        # Priority 1: Case C - Sustained Outward Shift (Requires ALL 4 conditions)
        r_consec = (k_z_r >= self.k_min_consecutive)
        m_consec = (k_z_m >= self.k_min_consecutive)
        
        if r_consec and m_consec and abs(z_r) > self.threshold and abs(z_m) > self.threshold and abs(z_cum) > self.threshold:
            return "Sustained outward shift relative to baseline detected."
            
        # Priority 2: Case A - Directional Tendency Without Expansion
        if r_consec and not m_consec:
            return "Directional tendency without measurable expansion."
            
        # Priority 3: Case B - Boundary Expansion Without Sustained Directional Drift
        if m_consec and not r_consec:
            return "Boundary expansion without sustained directional drift."
            
        # Priority 4: Transient Deviations (Spikes without consecutive gating)
        if (abs(z_r) > self.threshold or abs(z_m) > self.threshold) and not r_consec and not m_consec:
            return "Transient deviation observed. Monitor for persistence."
            
        # Priority 5: Variance expansion only
        if (vol_r > 0 or vol_m > 0):
            return "Elevated variability relative to expected fluctuation range."
            
        # Priority 6: None triggered
        return "Overall system state remains stable."

    def generate_clinical_report(self, row: pd.Series) -> dict:
        """
        Consumes a single row of computed statistics (containing deltas and Z-scores)
        and outputs the fully sanitized clinical dictionary.
        """
        report = {}
        
        report['Speed'] = self.translate_speed(row.get('k_z_delta_S', 0), row.get('z_delta_S', 0.0))
        report['Lateralization'] = self.translate_lateralization(row.get('k_z_delta_L', 0), row.get('z_delta_L', 0.0))
        report['Tone'] = self.translate_tone(row.get('k_z_delta_T', 0), row.get('z_delta_T', 0.0))
        
        report['GlobalState'] = self.translate_global_state(
            k_z_r=row.get('k_z_r', 0),
            k_z_m=row.get('k_z_delta_M', 0),
            z_r=row.get('z_r', 0.0),
            z_m=row.get('z_delta_M', 0.0),
            z_cum=row.get('z_cum_r', 0.0),
            vol_r=row.get('volatility_r_t', 0),
            vol_m=row.get('volatility_delta_M', 0)
        )
        
        return report
