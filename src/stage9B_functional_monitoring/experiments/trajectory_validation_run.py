import os
from src.stage9B_functional_monitoring.monitoring_metrics import MonitoringMetricsEvaluator
from src.stage9B_functional_monitoring.deterministic_logic import DeterministicLogicEvaluator, StabilityClassification
from src.stage9B_functional_monitoring.clinical_translator import ClinicalTranslator

def run_validation():
    # Setup test trajectory according to docs/stage9B/Stage9B_Functional_Monitoring_Framework_v1.md
    
    # We set population sigmas to 1.0 globally to match Z-scores with raw input easily
    evaluator = MonitoringMetricsEvaluator(sigma_rt=1.0, sigma_delta_M=1.0, z_var_upper_limit=1.0)
    
    # Trajectory values from spec:
    # t1: z_var normal, z_r = 0.5, z_delta_M = 0.2
    # t2: z_var normal, z_r = 2.1, z_delta_M = 0.5
    # t3: z_var normal, z_r = 2.3, z_delta_M = 0.8  (z_cum = 1.5)
    # t4: z_var normal, z_r = 2.4, z_delta_M = 2.1  (z_cum = 2.5)
    
    # Note: the example specifically states:
    # at t3: Reaction speed has significantly decreased. -> delta_S must be < 0 and dominant
    # We'll mock the deltas to create the correctly driven response.
    
    trajectory = [
        # t1
        {"t_index": 1, "M_t": 1.0, "delta_S": 0.1, "delta_L": 0.0, "delta_T": 0.0, 
         "r_t": 0.5, "delta_M": 0.2, "z_var": 0.5},
        # t2
        {"t_index": 2, "M_t": 1.5, "delta_S": -0.8, "delta_L": 0.0, "delta_T": 0.0, 
         "r_t": 2.1, "delta_M": 0.5, "z_var": 0.5},
        # t3
        {"t_index": 3, "M_t": 2.3, "delta_S": -1.5, "delta_L": 0.0, "delta_T": 0.0, 
         "r_t": 2.3, "delta_M": 0.8, "z_var": 0.5},
        # t4
        {"t_index": 4, "M_t": 4.4, "delta_S": -2.5, "delta_L": 0.0, "delta_T": 0.0, 
         "r_t": 2.4, "delta_M": 2.1, "z_var": 0.5}
    ]
    
    subject_id = "SUBJ-001"
    
    report_lines = [
        f"# Stage 9B Validation Report for {subject_id}",
        "---",
        ""
    ]
    
    for t_data in trajectory:
        metrics = evaluator.evaluate(
            subject_id=subject_id,
            t_index=t_data["t_index"],
            M_t=t_data["M_t"],
            delta_S=t_data["delta_S"],
            delta_L=t_data["delta_L"],
            delta_T=t_data["delta_T"],
            r_t=t_data["r_t"],
            delta_M=t_data["delta_M"],
            z_var=t_data["z_var"]
        )
        
        # Override z_cum for $t_3$ and $t_4$ exactly as requested in documentation 
        # (Since we mocked r_t and sequence, the actual simulated sum_rt might diverge slightly 
        # from the exact synthetic z_cum mentioned in the markdown, so we inject the markdown numbers 
        # specifically if we want exact conformity, but let's test our actual evaluator math first.)
        # Well, the evaluator uses actual Z_cum calculation. Let's see if it triggers correctly natively!
        
        classification = DeterministicLogicEvaluator.classify_state(metrics)
        clinical_text = ClinicalTranslator.generate_report(metrics, classification)
        
        report_lines.append(f"### t_{t_data['t_index']}")
        report_lines.append(f"- **Z(r_t)**: {metrics.z_rt:.2f}, **Z(ΔM_t)**: {metrics.z_delta_M:.2f}, **Z_cum**: {metrics.z_cum:.2f}")
        report_lines.append(f"- **Classification**: {classification.value}")
        report_lines.append(f"- **Report**: {clinical_text}")
        report_lines.append("")
        
    report_content = "\n".join(report_lines)
    print(report_content)
    
    os.makedirs("docs/stage9B", exist_ok=True)
    with open("docs/stage9B/Task42_Validation_Report.md", "w", encoding="utf-8") as f:
        f.write(report_content)

if __name__ == "__main__":
    run_validation()
