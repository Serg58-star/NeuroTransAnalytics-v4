"""
Baseline Feature Extractor for Exploratory Lab MVP (Corrected)

Computes 11 methodologically corrected features:
1. Median_ΔV1 (by visual field: left, center, right)
2. Asymmetry_ΔV1 (absolute and relative - corrected formulas)
3. MAD_ΔV1 - phase stability
4. ΔV4 (by visual field: left, right) - color processing delay
5. ΔV5 (by visual field: left, right) - motion detection delay
6. PSI_tau - cortical recovery time constant (exponential model)
7. PSI_slope_linear - cortical recovery speed (linear model, for comparison)

Methodological Corrections (Task 27.1):
- Asymmetry no longer uses center normalization
- Visual fields are NOT aggregated prematurely
- Exponential PSI recovery model added
"""

import numpy as np
import pandas as pd
from typing import Dict, Any
from scipy import stats
from scipy.optimize import curve_fit
import warnings


class BaselineFeatureExtractor:
    """
    Extracts 6 baseline features from trial-level data.
    
    This implementation follows the methodology outlined in Task_26_6,
    computing features across spatial fields and temporal dynamics.
    """
    
    def __init__(self):
        """Initialize the feature extractor."""
        pass
    
    def extract_subject_features(self, trials_df: pd.DataFrame) -> Dict[str, float]:
        """
        Extract all 11 corrected baseline features for a single subject.
        
        Parameters
        ----------
        trials_df : pd.DataFrame
            Trial-level data for one subject. Must contain columns:
            - stimulus_location (left/center/right)
            - stimulus_color
            - rt (reaction time, ms)
            - psi (pre-stimulus interval, ms)
            - is_outlier
            - test_type
        
        Returns
        -------
        dict
            Feature dictionary with corrected metrics:
            - median_dv1_left, median_dv1_center, median_dv1_right
            - asym_dv1_abs, asym_dv1_rel (corrected asymmetry)
            - mad_dv1 (global), mad_dv1_left, mad_dv1_center, mad_dv1_right (Task 27.2A)
            - delta_v4_left, delta_v4_center, delta_v4_right (center for validation only)
            - delta_v5_left, delta_v5_center, delta_v5_right (center for validation only)
            - psi_tau, psi_slope_linear
            
            Note: 17 total features (12 main + 2 validation center + 3 field-specific MAD)
        """
        # Filter outliers
        df_clean = trials_df[trials_df['is_outlier'] == False].copy()
        
        if len(df_clean) < 10:
            return self._empty_features()
        
        features = {}
        
        # 1. Extract ΔV1 components by field (NOT aggregated)
        dv1_by_field = self._compute_dv1_by_field(df_clean)
        
        # Store separate field values
        features['median_dv1_left'] = dv1_by_field.get('left', np.nan)
        features['median_dv1_center'] = dv1_by_field.get('center', np.nan)
        features['median_dv1_right'] = dv1_by_field.get('right', np.nan)
        
        # 2. CORRECTED Asymmetry_ΔV1 (Task 27.1)
        # No longer using center normalization
        left = dv1_by_field.get('left', np.nan)
        right = dv1_by_field.get('right', np.nan)
        
        if pd.notna(left) and pd.notna(right):
            # Absolute asymmetry
            features['asym_dv1_abs'] = abs(right - left)
            
            # Relative asymmetry (normalized by mean)
            mean_lr = (right + left) / 2
            if mean_lr > 0:
                features['asym_dv1_rel'] = (right - left) / mean_lr
            else:
                features['asym_dv1_rel'] = 0.0
        else:
            features['asym_dv1_abs'] = np.nan
            features['asym_dv1_rel'] = np.nan
        
        # 3. MAD_ΔV1 (global and per-field)
        dv1_all = df_clean[df_clean['test_type'] == 'Tst1']['rt']
        features['mad_dv1'] = self._median_absolute_deviation(dv1_all)
        
        # Task 27.2A: Field-specific MAD for multiple regression
        tst1 = df_clean[df_clean['test_type'] == 'Tst1']
        for location in ['left', 'center', 'right']:
            field_data = tst1[tst1['stimulus_location'] == location]['rt']
            features[f'mad_dv1_{location}'] = self._median_absolute_deviation(field_data)
        
        # 4. ΔV4 - Color processing delay (by visual field)
        dv4_by_field = self._compute_delta_v4_by_field(df_clean, dv1_by_field)
        features['delta_v4_left'] = dv4_by_field.get('left', np.nan)
        features['delta_v4_center'] = dv4_by_field.get('center', np.nan)  # Task 27.2: for validation
        features['delta_v4_right'] = dv4_by_field.get('right', np.nan)
        
        # 5. ΔV5 - Motion detection delay (by visual field)
        dv5_by_field = self._compute_delta_v5_by_field(df_clean, dv1_by_field)
        features['delta_v5_left'] = dv5_by_field.get('left', np.nan)
        features['delta_v5_center'] = dv5_by_field.get('center', np.nan)  # Task 27.2: for validation
        features['delta_v5_right'] = dv5_by_field.get('right', np.nan)
        
        # 6. PSI - Cortical recovery (exponential + linear)
        psi_results = self._compute_psi_models(df_clean)
        features['psi_tau'] = psi_results['tau']
        features['psi_slope_linear'] = psi_results['slope_linear']
        
        return features
    
    def _compute_dv1_by_field(self, df: pd.DataFrame) -> Dict[str, float]:
        """Compute ΔV1 (simple reaction time) for each visual field."""
        dv1_by_field = {}
        
        # ΔV1 = RT from simple reaction test (Tst1)
        tst1 = df[df['test_type'] == 'Tst1']
        
        for location in ['left', 'center', 'right']:
            field_data = tst1[tst1['stimulus_location'] == location]['rt']
            if len(field_data) >= 3:
                dv1_by_field[location] = np.median(field_data)
        
        return dv1_by_field
    
    def _median_absolute_deviation(self, data: pd.Series) -> float:
        """Compute median absolute deviation (MAD)."""
        if len(data) < 2:
            return 0.0
        median = np.median(data)
        mad = np.median(np.abs(data - median))
        return float(mad)
    
    def _compute_delta_v4_by_field(self, df: pd.DataFrame, 
                                    dv1_by_field: Dict[str, float]) -> Dict[str, float]:
        """
        Compute ΔV4 - color processing delay by visual field.
        
        ΔV4 = RT(red stimulus) - ΔV1 for each field.
        Red stimulus activates parvocellular pathway (acetylcholine modulation).
        
        Task 27.1: Separate by visual field, do NOT aggregate.
        """
        dv4_by_field = {}
        
        # RT for red stimuli (Tst2 - all red)
        tst2 = df[df['test_type'] == 'Tst2']
        
        # Task 27.2: Include center field for validation
        for location in ['left', 'center', 'right']:
            field_data = tst2[tst2['stimulus_location'] == location]['rt']
            if len(field_data) >= 3 and location in dv1_by_field:
                rt_red = np.median(field_data)
                dv4_by_field[location] = rt_red - dv1_by_field[location]
        
        return dv4_by_field
    
    def _compute_delta_v5_by_field(self, df: pd.DataFrame, 
                                    dv1_by_field: Dict[str, float]) -> Dict[str, float]:
        """
        Compute ΔV5 - motion detection delay by visual field.
        
        ΔV5 = RT(shift test) - ΔV1 for each field.
        Shift test activates magnocellular pathway (dopamine modulation).
        
        Task 27.1: Separate by visual field, do NOT aggregate.
        """
        dv5_by_field = {}
        
        # RT for shift test (Tst3 - motion detection)
        tst3 = df[df['test_type'] == 'Tst3']
        
        # Task 27.2: Include center field for validation
        for location in ['left', 'center', 'right']:
            field_data = tst3[tst3['stimulus_location'] == location]['rt']
            if len(field_data) >= 3 and location in dv1_by_field:
                rt_shift = np.median(field_data)
                dv5_by_field[location] = rt_shift - dv1_by_field[location]
        
        return dv5_by_field
    
    def _compute_psi_models(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        Compute PSI models - cortical recovery dynamics.
        
        Task 27.1: Implements both exponential and linear models.
        
        Exponential model: RT(PSI) = RT₀ + β * exp(-PSI / τ)
        Linear model: RT ~ PSI (for comparison)
        
        Returns tau (recovery time constant) and linear slope.
        """
        results = {'tau': np.nan, 'slope_linear': np.nan}
        
        # Filter for valid PSI and RT
        valid_data = df[(df['psi'].notna()) & (df['rt'].notna())].copy()
        
        if len(valid_data) < 10:
            return results
        
        psi_values = valid_data['psi'].values
        rt_values = valid_data['rt'].values
        
        # 1. Linear model (baseline)
        try:
            slope, _, _, _, _ = stats.linregress(psi_values, rt_values)
            results['slope_linear'] = float(slope)
        except:
            pass
        
        # 2. Exponential model (Task 27.1)
        # RT(PSI) = RT₀ + β * exp(-PSI / τ)
        if len(valid_data) >= 15:  # Require more points for stable exponential fit
            try:
                results['tau'] = self._fit_exponential_recovery(psi_values, rt_values)
            except:
                pass  # Fallback to NaN if fitting fails
        
        return results
    
    def _fit_exponential_recovery(self, psi: np.ndarray, rt: np.ndarray) -> float:
        """
        Fit exponential recovery model and extract tau parameter.
        
        Model: RT(PSI) = RT₀ + β * exp(-PSI / τ)
        
        Returns
        -------
        float
            tau - recovery time constant (ms)
        """
        def exp_recovery(psi, rt0, beta, tau):
            """Exponential recovery function."""
            return rt0 + beta * np.exp(-psi / tau)
        
        # Initial parameter guesses
        rt_min = np.min(rt)
        rt_max = np.max(rt)
        psi_range = np.max(psi) - np.min(psi)
        
        p0 = [
            rt_min,           # RT₀ (baseline RT at infinite PSI)
            rt_max - rt_min,  # β (amplitude of recovery)
            psi_range / 2     # τ (time constant, guess half of PSI range)
        ]
        
        # Bounds: RT₀ > 0, β > 0, τ > 0
        bounds = ([0, 0, 1], [np.inf, np.inf, 10000])
        
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                popt, _ = curve_fit(exp_recovery, psi, rt, p0=p0, bounds=bounds, maxfev=2000)
                tau = popt[2]
                
                # Sanity check: tau should be reasonable (10-2000 ms)
                if 10 <= tau <= 2000:
                    return float(tau)
                else:
                    return np.nan
        except:
            return np.nan
    
    def _empty_features(self) -> Dict[str, float]:
        """Return empty feature dict with NaN values (17 features: 12 main + 2 validation + 3 field MAD)."""
        return {
            'median_dv1_left': np.nan,
            'median_dv1_center': np.nan,
            'median_dv1_right': np.nan,
            'asym_dv1_abs': np.nan,
            'asym_dv1_rel': np.nan,
            'mad_dv1': np.nan,
            'mad_dv1_left': np.nan,  # Task 27.2A: field-specific MAD
            'mad_dv1_center': np.nan,  # Task 27.2A: field-specific MAD
            'mad_dv1_right': np.nan,  # Task 27.2A: field-specific MAD
            'delta_v4_left': np.nan,
            'delta_v4_center': np.nan,  # Task 27.2: validation-only
            'delta_v4_right': np.nan,
            'delta_v5_left': np.nan,
            'delta_v5_center': np.nan,  # Task 27.2: validation-only
            'delta_v5_right': np.nan,
            'psi_tau': np.nan,
            'psi_slope_linear': np.nan
        }
    
    def extract_population_features(self, trials_df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract features for all subjects in the dataset.
        
        Parameters
        ----------
        trials_df : pd.DataFrame
            Trial-level data for multiple subjects.
        
        Returns
        -------
        pd.DataFrame
            Feature matrix with subjects as rows and features as columns.
            Index is subject_id.
        """
        features_list = []
        
        for subject_id, subject_trials in trials_df.groupby('subject_id'):
            features = self.extract_subject_features(subject_trials)
            features['subject_id'] = subject_id
            features_list.append(features)
        
        features_df = pd.DataFrame(features_list)
        features_df = features_df.set_index('subject_id')
        
        # Drop subjects with any NaN features  
        features_df = features_df.dropna()
        
        return features_df
