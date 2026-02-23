from enum import Enum
from .monitoring_metrics import MonitoringMetrics

class StabilityClassification(Enum):
    VOLATILE_STRUCTURAL = "Volatile (Structural)"
    EXPANDING_BOUNDARY = "Expanding boundary"
    DIRECTIONALLY_SHIFTING = "Directionally shifting"
    VOLATILE_TRANSIENT = "Volatile (Transient)"
    STABLE = "Stable"

class DeterministicLogicEvaluator:
    """
    Evaluates MonitoringMetrics against a strict rule-based hierarchy to 
    classify the subject's longitudinal state in Stage 9B.
    """
    
    @staticmethod
    def classify_state(metrics: MonitoringMetrics) -> StabilityClassification:
        # Decision Logic Flow: Top-to-bottom evaluation.
        
        # 1. Variance shift exceeds 95th percentile
        if metrics.z_var > metrics.z_var_upper_bound:
            return StabilityClassification.VOLATILE_STRUCTURAL
            
        # Helper conditions
        r_t_significant = abs(metrics.z_rt) > 1.96
        delta_M_t_significant = abs(metrics.z_delta_M) > 1.96
        z_cum_significant = abs(metrics.z_cum) > 1.96
        
        consecutive_r_t = metrics.consecutive_z_rt_count >= metrics.k_min_consecutive
        consecutive_delta_M = metrics.consecutive_z_delta_M_count >= metrics.k_min_consecutive
        
        # 2. Expanding boundary (Case C: both direction & expansion sustained)
        if consecutive_r_t and z_cum_significant and delta_M_t_significant:
            return StabilityClassification.EXPANDING_BOUNDARY
            
        # 3. Expanding boundary (Case B: boundary expands without directional drift)
        if consecutive_delta_M and not r_t_significant:
            return StabilityClassification.EXPANDING_BOUNDARY
            
        # 4. Directionally shifting (Case A: direction tending without measurable expansion)
        if consecutive_r_t and not delta_M_t_significant:
            return StabilityClassification.DIRECTIONALLY_SHIFTING
            
        # 5. Single isolated transient event (k < k_min_consecutive)
        if r_t_significant or delta_M_t_significant or z_cum_significant:
            return StabilityClassification.VOLATILE_TRANSIENT
            
        # 6. Default to Stable
        return StabilityClassification.STABLE
