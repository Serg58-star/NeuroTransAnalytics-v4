import pytest
import numpy as np
import pandas as pd
from src.stage9A_v5_architecture.dual_space_core import (
    compute_robust_layer,
    compute_robust_z_layer,
    apply_local_donders,
    compute_analytical_space,
    compute_global_modulator,
    apply_load_operator
)

@pytest.fixture
def synthetic_trial_data():
    """
    Generates heavy-tail RT data to rigorously test the Median/MAD independence from Mean.
    """
    np.random.seed(42)
    channels = ['V1', 'Parvo', 'Magno', 'Koniocellular']
    positions = ['L', 'C', 'R']
    
    data = []
    
    for ch in channels:
        for pos in positions:
            # Baseline RTs around 250ms
            normal_rts = np.random.normal(250, 15, 10).tolist()
            # 2 extreme burst anomalies
            burst_rts = [900, 1100]
            
            # Combine 12 trials
            rts = normal_rts + burst_rts
            
            for rt in rts:
                data.append({
                    'Stimulus': ch,
                    'Position': pos,
                    'RT': rt
                })
                
    return pd.DataFrame(data)

def test_robust_estimation_layer(synthetic_trial_data):
    """
    Testing Level I: Median/MAD over Heavy Tail data.
    """
    robust_space = compute_robust_layer(synthetic_trial_data)
    
    # Assert dimensions (4 channels * 3 positions)
    assert len(robust_space) == 4
    for ch in robust_space:
        assert len(robust_space[ch]) == 3
        
    # Analyze bursting behavior on V1 - L
    subset = synthetic_trial_data[(synthetic_trial_data['Stimulus'] == 'V1') & (synthetic_trial_data['Position'] == 'L')]
    true_mean = subset['RT'].mean()
    true_median = subset['RT'].median()
    
    calc_median = robust_space['V1']['L']['median']
    
    # Assert we did NOT use mean for the median slot
    assert calc_median == pytest.approx(true_median)
    assert calc_median != pytest.approx(true_mean)
    
    # Mean is highly pulled by bursts (e.g. mean ~370, median ~250)
    assert true_mean > true_median + 50 

def test_local_donders(synthetic_trial_data):
    """
    Testing Level IV: Donders invariance (Within-field only).
    """
    robust_space = compute_robust_layer(synthetic_trial_data)
    donders_space = apply_local_donders(robust_space, base_channel='V1')
    
    assert 'V1' not in donders_space
    assert 'Parvo' in donders_space
    assert 'Magno' in donders_space
    assert 'Koniocellular' in donders_space
    
    # Check that calculation is strictly Parvo L - V1 L
    expected_p_l = robust_space['Parvo']['L']['median'] - robust_space['V1']['L']['median']
    expected_p_c = robust_space['Parvo']['C']['median'] - robust_space['V1']['C']['median']
    
    assert donders_space['Parvo']['L'] == pytest.approx(expected_p_l)
    assert donders_space['Parvo']['C'] == pytest.approx(expected_p_c)

def test_robust_z_layer(synthetic_trial_data):
    """
    Testing Level II.5: Dimensionless Standardization.
    """
    robust_space = compute_robust_layer(synthetic_trial_data)
    z_space = compute_robust_z_layer(robust_space)
    
    # Assert Z-space calculation logic
    med_L = robust_space['V1']['L']['median']
    med_C = robust_space['V1']['C']['median']
    med_R = robust_space['V1']['R']['median']
    
    global_v1_median = np.median([med_L, med_C, med_R])
    expected_z_L = (med_L - global_v1_median) / robust_space['V1']['L']['mad']
    
    assert z_space['V1']['L'] == pytest.approx(expected_z_L)

def test_analytical_space(synthetic_trial_data):
    """
    Testing Level III: Orthogonal Geometry.
    """
    robust_space = compute_robust_layer(synthetic_trial_data)
    z_space = compute_robust_z_layer(robust_space)
    analytical_space = compute_analytical_space(z_space)
    
    v1_analytical = analytical_space['V1']
    
    # Extract Z-scores
    L = z_space['V1']['L']
    C = z_space['V1']['C']
    R = z_space['V1']['R']
    
    # Assert Center is the average of the Z-scores
    expected_center = np.mean([L, C, R])
    assert v1_analytical['Center_X'] == pytest.approx(expected_center)
    
    # Assert Lateralization anchors to Z-Center
    assert v1_analytical['Lat_X_L'] == pytest.approx(L - C)
    assert v1_analytical['Lat_X_R'] == pytest.approx(R - C)
    
def test_global_modulator(synthetic_trial_data):
    """
    Testing Level V & VI: G formulation
    """
    robust_space = compute_robust_layer(synthetic_trial_data)
    z_space = compute_robust_z_layer(robust_space)
    analytical_space = compute_analytical_space(z_space)
    
    weights = {'V1': 0.1, 'Parvo': 0.2, 'Magno': 0.5, 'Koniocellular': 0.2}
    
    g_val = compute_global_modulator(analytical_space, weights)
    
    expected_g = (analytical_space['V1']['Center_X'] * 0.1 + 
                  analytical_space['Parvo']['Center_X'] * 0.2 +
                  analytical_space['Magno']['Center_X'] * 0.5 +
                  analytical_space['Koniocellular']['Center_X'] * 0.2)
                  
    assert g_val == pytest.approx(expected_g)

def test_phase_2_operator():
    """
    Testing Level VII: Linear F2 load in Z-space.
    """
    # Simulate Phase 1 physiological center vector IN Z-SPACE
    Z_F1 = {'V1': 0.1, 'Parvo': 0.5, 'Magno': -0.2, 'Koniocellular': 1.2}
    
    # Lambda Level 1 Load
    lamb = 1.0 
    
    # Sensitivity (e.g. Parvo is highly sensitive to load, V1 is not)
    sens = {'V1': 0.0, 'Parvo': 0.3, 'Magno': 0.1, 'Koniocellular': 0.5}
    
    Z_F2 = apply_load_operator(Z_F1, lamb, sens)
    
    assert Z_F2['V1'] == 0.1
    assert Z_F2['Parvo'] == pytest.approx(0.8)
    assert Z_F2['Koniocellular'] == pytest.approx(1.7)
