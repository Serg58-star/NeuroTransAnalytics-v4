import os
from src.c3_core.etl.etl_v4 import ETLPipeline
from src.c3_core.component_timing.component_v4 import ComponentTimingV4
from src.c3_core.qc_aggregation.qc_aggregation_v4 import QCAggregationV4
from src.c3_core.scenario_engine.scenario_v4 import ScenarioEngineV4

def prepare_data():
    print("--- Running C3 Pipeline ---")
    
    # 1. ETL
    etl = ETLPipeline(db_path="neuro_data.db")
    event_frame = etl.run()
    
    # 2. Component Timing
    comp = ComponentTimingV4()
    component_frame = comp.run(event_frame)
    
    # 3. QC Aggregation
    qc_agg = QCAggregationV4()
    aggregated_frame = qc_agg.run(component_frame)
    
    # 4. Scenario Engine
    engine = ScenarioEngineV4()
    results = engine.run(aggregated_frame)
    
    # 5. Export
    output_dir = "data/derived/scenarios"
    engine.export_results(results, output_dir)
    
    print("\n--- Data Preparation Complete ---")

if __name__ == "__main__":
    prepare_data()
