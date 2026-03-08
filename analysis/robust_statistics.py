import numpy as np
import pandas as pd

def median_value(data):
    """Calculate the robust central tendency (median)."""
    if isinstance(data, (pd.Series, pd.DataFrame)):
        return data.median()
    return np.median(data)

def mad_value(data):
    """Calculate the Median Absolute Deviation (MAD)."""
    if isinstance(data, (pd.Series, pd.DataFrame)):
        data = data.dropna()
    else:
        # Convert to numpy array and drop nans
        data = np.asarray(data)
        data = data[~np.isnan(data)]
        
    if len(data) == 0:
        return np.nan
        
    med = np.median(data)
    # Using the standard MAD calculation without the 1.4826 normal-consistency multiplier
    # as the baseline metrics just use median absolute difference.
    # If the user's specific context needs normal-consistent MAD, we would multiply by 1.4826
    mad = np.median(np.abs(data - med))
    return mad

def iqr_value(data):
    """Calculate the Interquartile Range (IQR)."""
    if isinstance(data, (pd.Series, pd.DataFrame)):
        data = data.dropna()
    else:
        data = np.asarray(data)
        data = data[~np.isnan(data)]
        
    if len(data) == 0:
        return np.nan
        
    q75, q25 = np.percentile(data, [75 ,25])
    return q75 - q25

def percentile_range(data, p_low, p_high):
    """Calculate a specific percentile range [p_low, p_high]."""
    if isinstance(data, (pd.Series, pd.DataFrame)):
        data = data.dropna()
    else:
        data = np.asarray(data)
        data = data[~np.isnan(data)]
        
    if len(data) == 0:
        return (np.nan, np.nan)
        
    return tuple(np.percentile(data, [p_low, p_high]))
