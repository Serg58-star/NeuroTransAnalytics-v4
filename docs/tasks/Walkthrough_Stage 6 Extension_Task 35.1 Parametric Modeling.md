Walkthrough: Stage 6 Extension (Task 35.1 Parametric Modeling)
This walkthrough documents the completion of Task 35.1, an extension block in Stage 6 evaluating generative parameter fitting of Reaction Times. The objective was to determine whether a specific generative law accurately models RT data across the tests, adhering to a strict non-interpretative and synthetic-first framework.

1. Synthetic Parameters & Generator Validation
To preserve isolation, standard libraries (
c3x_exploratory/synthetic_parametric.py
) were created mapping exactly to robust generative specifications:

Normal Sequence Generator
Lognormal Sequence Generator
Gamma Sequence Generator
Weibull Sequence Generator
Exponentially Modified Gaussian (Ex-Gaussian) Generator
The exploratory procedure natively fitted all parameterized shapes:

NOTE

All synthetic integration tests passed pytest tests/test_c3x_parametric.py. Lognormal inputs correctly recognized Lognormal fitting superiority, protecting algorithmic integrity prior to execution.

2. Real Data Execution & Output (Testing_RT)
The validation script 
scripts/run_stage6_parametric.py
 successfully processed valid RT sequences spanning $N=4464$ instances across subjects.

Population Dominance Results
The fit comparison generated explicit maximum likelihood metrics per sequence:

Dominant Model by AIC (Akaike Information Criterion):

Normal: 52.8%
Ex-Gaussian: 40.9%
Lognormal: 4.5%
Weibull: 1.5%
Gamma: 0.3%
Dominant Model by BIC (Bayesian Information Criterion):

Normal: 66.8%
Ex-Gaussian: 31.5%
Lognormal: 1.1%
Weibull: 0.5%
Gamma: 0.1%
3. Structural Conclusion
IMPORTANT

The heavy-tail geometry identified in previous steps does not strictly manifest as lognormality. Normal and Ex-Gaussian parametric structures are heavily dominant functionally when applied directly onto trial-level sequences.

Generative Architecture Impact:

Lognormal does NOT dominate. The multiplicative noise model is statistically weaker than additive bounded models for trial-level sequences in NeuroTransAnalytics-v4.
Ex-Gaussian vs Normal Trade-off. The penalty for added parameters (seen in BIC penalizing Ex-Gaussian relative to AIC) indicates that for the majority of sequences, the base normal distribution structurally absorbs the bulk variance. Ex-Gaussian strongly defines a large sub-population (30-40%), likely tracking states with rare delay mechanisms.
This concludes Task 35.1. The procedure executed exclusively in a read-only capacity relative to the canonical SQLite storage.