4. Ex-Gaussian Parametric Integration (Task 35.2)
To finalize the parametric investigation in Stage 6, we isolated the Sub-population (~31-41%) where the Exponentially Modified Gaussian (Ex-Gaussian) distribution provided the best structural fit. The objective was to determine whether the exponential tail parameter ($\tau$) forms a distinct new latent axis, or if it collapses into preexisting macro/micro axes.

An exploratory integration check (
c3x_exploratory/exgaussian_integration.py
) extracted $\mu$, $\sigma$, and $\tau$ over the database, calculating rank correlations and an extended component matrix against basic Macro features (Speed via median_rt) and Micro/Tail features (burst_freq, skewness).

Output Correlation Matrix (Spearman)
median_rt    tau     mu  sigma  burst_freq  skewness
median_rt       1.000  0.273  0.959  0.683      -0.069    -0.188    
tau             0.273  1.000  0.038 -0.189       0.002     0.721    
mu              0.959  0.038  1.000  0.761      -0.078    -0.372    
sigma           0.683 -0.189  0.761  1.000      -0.040    -0.621    
burst_freq     -0.069  0.002 -0.078 -0.040       1.000     0.040    
skewness       -0.188  0.721 -0.372 -0.621       0.040     1.000
Extended PCA Eigenvalues
Eigenvalues: [2.844, 1.595, 0.999, 0.324, 0.237, 0.002]

Architectural Conclusion
IMPORTANT

No New Axis Forms: The parameter $\tau$ does NOT create a new latent dimension.

$\mu$ is structurally entangled with median_rt ($r=0.959$). It simply reproduces the Macro Speed Axis.
$\tau$ is strictly structurally coupled with non-parametric skewness ($r=0.721$).
$\tau$ possesses effectively zero correlation with burst_freq ($r=0.002$), proving that Ex-Gaussian tails are NOT tracking intra-sequence microdynamic state-transitions.
The PCA yields an eigenvalue of 0.002, highlighting strict collinearity/redundancy in the expanded matrix.
Integrating the Ex-Gaussian formalization is structurally redundant to the established 7-dimensional geometry and tail indices. The Stage 6 Exploratory branch is closed.
