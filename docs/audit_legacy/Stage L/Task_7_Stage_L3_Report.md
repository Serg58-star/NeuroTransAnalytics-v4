# Task 7 Stage L3 Report — Visual Pattern Exploration
    
Dataset: `neuro_data.db`
Generated automatically by `run_stage_L3.py`.

## Executed Queries
The visualizations below are derived from `reactions_view`, converting the wide-format Boxbase `trials` output into a long-format event table to enable pattern exploration. Error plots utilize trial-level error counters directly from the database schema.

## 1. RT Distribution
![rt_distribution](figures/rt_distribution.png)  
![rt_distribution_by_test](figures/rt_distribution_by_test.png)  
*Observational Note: Mean RT differs visibly between test types.*

## 2. RT vs PSI
![rt_vs_psi](figures/rt_vs_psi.png)  
*Observational Note: RT values show visible spread and variation across the different PSI levels.*

## 3. RT vs Visual Field
![rt_vs_field](figures/rt_vs_field.png)  
*Observational Note: The descriptive statistics indicate variations in median reaction time based on visual field presentation.*

## 4. RT vs Stimulus Index
![rt_vs_index](figures/rt_vs_index.png)  
*Observational Note: Mean reaction time fluctuates dynamically in an oscillatory pattern throughout the ordered sequence of 36 stimuli.*

## 5. RT vs Test Type
![rt_vs_test_type](figures/rt_vs_test_type.png)  
*Observational Note: Distinct bands of average RT are observable corresponding to each test type (simple, shift, color).*

## 6. Error Structure
![errors_by_test_type](figures/errors_by_test_type.png)  
*Observational Note: Premature error counts exhibit structural differences across the three test types.*
