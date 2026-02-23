from dataclasses import dataclass
from typing import Optional

@dataclass
class MonitoringMetrics:
    """
    Data payload holding the fluctuation metrics and state for a subject at time t.
    """
    subject_id: str
    t_index: int
    
    # Base Values
    M_t: float
    delta_S: float
    delta_L: float
    delta_T: float
    r_t: float
    delta_M: float
    
    # Statistical Values
    z_var: float
    z_rt: float
    z_delta_M: float
    z_cum: float
    
    # Gating and Counters
    consecutive_z_rt_count: int
    consecutive_z_delta_M_count: int
    
    # Config parameters representing empirical limits
    z_var_upper_bound: float = 1.0  # Normalized so > 1.0 means elevated (95th percentile)
    k_min_consecutive: int = 2

class MonitoringMetricsEvaluator:
    """
    Evaluates sequences of raw tracking values into formal MonitoringMetrics.
    Maintains the state to accumulate Z_cum and consecutive gating counts.
    """
    def __init__(self, sigma_rt: float, sigma_delta_M: float, z_var_upper_limit: float = 1.0):
        # We protect against division by zero
        self.sigma_rt = max(sigma_rt, 1e-9)
        self.sigma_delta_M = max(sigma_delta_M, 1e-9)
        self.z_var_upper_limit = z_var_upper_limit
        
        # State tracking per subject
        self._states = {}
        
    def evaluate(self, subject_id: str, t_index: int, 
                 M_t: float, delta_S: float, delta_L: float, delta_T: float,
                 r_t: float, delta_M: float, z_var: float) -> MonitoringMetrics:
        """
        Process the new incoming observation for the given subject.
        """
        if subject_id not in self._states:
            self._states[subject_id] = {
                'sum_rt': 0.0,
                'count': 0,
                'consecutive_z_rt': 0,
                'consecutive_z_delta_M': 0
            }
            
        state = self._states[subject_id]
        
        # Update running cumulative stats
        state['sum_rt'] += r_t
        state['count'] += 1
        
        # Compute current Z scores
        z_rt = r_t / self.sigma_rt
        z_delta_M = delta_M / self.sigma_delta_M
        
        # Compute cumulative Z score (Z_cum)
        # Z_cum = (Sum r_k) / sqrt(T * sigma_r^2)
        variance_cum = state['count'] * (self.sigma_rt ** 2)
        z_cum = state['sum_rt'] / (variance_cum ** 0.5) if variance_cum > 0 else 0.0
        
        # Update consecutive counters
        if abs(z_rt) > 1.96:
            state['consecutive_z_rt'] += 1
        else:
            state['consecutive_z_rt'] = 0
            
        if abs(z_delta_M) > 1.96:
            state['consecutive_z_delta_M'] += 1
        else:
            state['consecutive_z_delta_M'] = 0
            
        metrics = MonitoringMetrics(
            subject_id=subject_id,
            t_index=t_index,
            M_t=M_t,
            delta_S=delta_S,
            delta_L=delta_L,
            delta_T=delta_T,
            r_t=r_t,
            delta_M=delta_M,
            z_var=z_var,
            z_rt=z_rt,
            z_delta_M=z_delta_M,
            z_cum=z_cum,
            consecutive_z_rt_count=state['consecutive_z_rt'],
            consecutive_z_delta_M_count=state['consecutive_z_delta_M'],
            z_var_upper_bound=self.z_var_upper_limit
        )
        return metrics
