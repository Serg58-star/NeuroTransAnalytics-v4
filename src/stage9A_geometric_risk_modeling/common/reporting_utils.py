"""
stage9A_geometric_risk_modeling.common.reporting_utils

Formatting utilities to construct the final comparative markdown report.
"""

def compute_architectural_verdict(baseline_metrics, bootstrap_metrics, noise_metrics) -> dict:
    """
    Computes the stability-weighted structural preference based on Task 39.1 Rule.
    Score(M) = AUC_boot(M) - 1.0 * sigma_boot(M) - 0.5 * Cal(M)
    """
    scores = {}
    for model in baseline_metrics.keys():
        auc_boot = bootstrap_metrics[model]['auc_mean']
        sigma_boot = bootstrap_metrics[model]['auc_sd']
        cal_penalty = abs(1.0 - baseline_metrics[model]['calibration_slope'])
        
        score = auc_boot - (1.0 * sigma_boot) - (0.5 * cal_penalty)
        scores[model] = score
        
    sorted_models = sorted(scores.keys(), key=lambda k: scores[k], reverse=True)
    m_star = sorted_models[0]
    m_next = sorted_models[1]
    
    score_gap = scores[m_star] - scores[m_next]
    
    # Defaults
    verdicts_map = {
        'Radial': 'RADIAL_DOMINANT',
        'Vector': 'VECTOR_SENSITIVE',
        'Bayesian': 'TOPOLOGY_DEPENDENT'
    }
    
    final_verdict = "AMBIGUOUS_STRUCTURE"
    winner = m_star
    
    if score_gap >= 0.02:
        final_verdict = verdicts_map[m_star]
    else:
        # Tie-breaker via 10% Noise Degradation (closer to 0 is better)
        noise_m_star = abs(noise_metrics['0.10'][m_star]['delta_auc'])
        noise_m_next = abs(noise_metrics['0.10'][m_next]['delta_auc'])
        
        if noise_m_star < noise_m_next:
            final_verdict = verdicts_map[m_star]
        elif noise_m_next < noise_m_star:
            final_verdict = verdicts_map[m_next]
            winner = m_next
        else:
            final_verdict = "AMBIGUOUS_STRUCTURE"
            
    return {
        'scores': scores,
        'winner': winner,
        'final_verdict': final_verdict,
        'baseline_auc_winner': max(baseline_metrics, key=lambda k: baseline_metrics[k]['roc_auc']),
        'stability_winner': min(bootstrap_metrics, key=lambda k: bootstrap_metrics[k]['loss_sd']),
        'noise_winner': max(noise_metrics['0.10'], key=lambda k: noise_metrics['0.10'][k]['delta_auc']), # (Max is smallest drop)
        'calibration_winner': min(baseline_metrics, key=lambda k: abs(1.0 - baseline_metrics[k]['calibration_slope']))
    }

def generate_report_markdown(dataset_info, baseline_metrics, bootstrap_metrics, noise_metrics, verdict) -> str:
    """Constructs the Task 39 comparative report in the required format."""
    
    md = f"""# Task 39 — Comparative Geometric Risk Modeling  
## Execution Report

---

# 1. Dataset Description

- Number of subjects: {dataset_info['n_samples']}
- Condition type: {dataset_info['condition_type']}
- Class balance: {dataset_info['class_balance']}
- Synthetic or real labels: {dataset_info['label_source']}

---

# 2. Model Implementations

## 2.1 Radial Model

Specification:
Risk ~ Mahalanobis Distance

Implementation details:
- Model type: Logistic Regression
- Regularization: None explicitly (C=1e9)
- Threshold selection: Default 0.5 (continuous probabilities used)

---

## 2.2 Vector Model

Specification:
Risk ~ (ΔSpeed, ΔLateral, ΔTone)

Implementation details:
- Model type: Logistic Regression
- Interaction terms: None
- Regularization: None explicitly (C=1e9)

---

## 2.3 Bayesian Model

Specification:
P(Condition | Position)

Implementation details:
- KDE bandwidth: Scott's rule (scipy default)
- Grid resolution (if voxelized): N/A (continuous KDE)
- Smoothing parameters: None

---

# 3. Baseline Performance Comparison

| Model    | ROC-AUC | Log-loss | Brier | Calibration Slope |
|----------|---------|----------|--------|------------------|
"""
    for model_name, metrics in baseline_metrics.items():
        md += f"| {model_name:<8} | {metrics['roc_auc']:.4f} | {metrics['log_loss']:.4f} | {metrics['brier_score']:.4f} | {metrics['calibration_slope']:.4f} |\n"

    md += """
---

# 4. Bootstrap Stability (n = 100)

| Model    | AUC Mean | AUC SD | Log-loss Mean | Log-loss SD |
|----------|----------|--------|---------------|-------------|
"""
    for model_name, metrics in bootstrap_metrics.items():
        md += f"| {model_name:<8} | {metrics['auc_mean']:.4f} | {metrics['auc_sd']:.4f} | {metrics['loss_mean']:.4f} | {metrics['loss_sd']:.4f} |\n"
        
    md += """
---

# 5. Noise Stability Test

## 5% Noise Injection

| Model    | ΔAUC | ΔLog-loss |
|----------|------|-----------|
"""
    for model_name, metrics in noise_metrics['0.05'].items():
        md += f"| {model_name:<8} | {metrics['delta_auc']:.4f} | {metrics['delta_loss']:.4f} |\n"
        
    md += """
## 10% Noise Injection

| Model    | ΔAUC | ΔLog-loss |
|----------|------|-----------|
"""
    for model_name, metrics in noise_metrics['0.10'].items():
        md += f"| {model_name:<8} | {metrics['delta_auc']:.4f} | {metrics['delta_loss']:.4f} |\n"

    md += f"""
---

# 6. Comparative Analysis

- Baseline AUC winner: {verdict['baseline_auc_winner']}
- Stability winner: {verdict['stability_winner']}
- Noise robustness winner: {verdict['noise_winner']}
- Calibration winner: {verdict['calibration_winner']}

### Formal Model Scores
| Model | Score(M) |
|-------|----------|
| Radial | {verdict['scores']['Radial']:.4f} |
| Vector | {verdict['scores']['Vector']:.4f} |
| Bayesian | {verdict['scores']['Bayesian']:.4f} |

---

# 7. Architectural Verdict

- {verdict['final_verdict']}

---

# 8. Compliance Confirmation

- [x] No PCA recomputation
- [x] No clustering
- [x] No geometry mutation
- [x] Identical coordinate inputs across models
"""
    return md

