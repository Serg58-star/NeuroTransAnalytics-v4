from .monitoring_metrics import MonitoringMetrics
from .deterministic_logic import StabilityClassification

class ClinicalTranslator:
    """
    Translates the structural classifications and raw metrics into
    safe, standardized patient-friendly language. Prohibits diagnostic terms.
    """
    
    # Strictly defined translation mappings from Stage 9B Framework specifications
    CLASSIFICATION_TEXTS = {
        StabilityClassification.VOLATILE_STRUCTURAL: "Elevated variability relative to expected fluctuation range.",
        StabilityClassification.EXPANDING_BOUNDARY: {
            "case_c": "Sustained outward shift relative to baseline detected.",
            "case_b": "Boundary expansion without sustained directional drift."
        },
        StabilityClassification.DIRECTIONALLY_SHIFTING: "Directional tendency without measurable expansion.",
        StabilityClassification.VOLATILE_TRANSIENT: "Transient deviation observed. Monitor for persistence.",
        StabilityClassification.STABLE: "Overall system state remains stable."
    }
    
    @staticmethod
    def generate_report(metrics: MonitoringMetrics, classification: StabilityClassification) -> str:
        base_text = ""
        
        # Resolve dynamic routing for EXPANDING_BOUNDARY
        if classification == StabilityClassification.EXPANDING_BOUNDARY:
            if metrics.consecutive_z_rt_count >= metrics.k_min_consecutive:
                base_text = ClinicalTranslator.CLASSIFICATION_TEXTS[classification]["case_c"]
            else:
                base_text = ClinicalTranslator.CLASSIFICATION_TEXTS[classification]["case_b"]
        else:
            base_text = ClinicalTranslator.CLASSIFICATION_TEXTS[classification]
            
        axis_translation = ClinicalTranslator._generate_axis_translations(metrics, classification)
        
        if axis_translation:
            return f"{base_text} {axis_translation}"
            
        return base_text
        
    @staticmethod
    def _generate_axis_translations(metrics: MonitoringMetrics, classification: StabilityClassification) -> str:
        # Axis translations are typically appended when clear directional shifts or transient shifts occur.
        # But we must only output primary axis shifts when they are part of a deviation that merits mention.
        if classification == StabilityClassification.STABLE:
            return ""
            
        # Identify dominant axis purely numerically to translate direction
        highest_delta = max(abs(metrics.delta_S), abs(metrics.delta_L), abs(metrics.delta_T))
        translations = []
        
        # We append translation ONLY for axes with measurable contributions (this is heuristic for translation, not structural logic).
        # We assume checking the actual sign (+/-) determines the translation wording.
        
        if abs(metrics.delta_S) == highest_delta and highest_delta > 0:
            if metrics.delta_S > 0:
                translations.append("Reaction speed has significantly increased.")
            else:
                translations.append("Reaction speed has significantly decreased.")
                
        if abs(metrics.delta_L) == highest_delta and highest_delta > 0:
            if metrics.delta_L > 0:
                translations.append("Interhemispheric synchrony improved.") # Or 'decreased', depending on exact L domain semantics.
                                                                            # We map delta L > 0 to improved for this draft, or we map explicitly based on spec.
                                                                            # Spec says: "[improved/decreased]"
            else:
                translations.append("Interhemispheric synchrony decreased.")
                
        if abs(metrics.delta_T) == highest_delta and highest_delta > 0:
            if metrics.delta_T > 0:
                translations.append("Functional tone increased.")
            else:
                translations.append("Functional tone decreased.")
                
        return " ".join(translations)
