# H2.2b Block 0 — Sample Construction

**Date**: 2026-03-03  
**Status**: COMPLETED  
**Basis**: Stage H2.2b — Subject-Level Spectral Recalculation

---

## Scope

Deduplication of the dataset to enforce strict subject-level geometry by retaining only the very first test visit (`test_date` / `test_time`) for each `subject_id`.

## Deduplication Metrics

| Metric | Value |
| :--- | :---: |
| **Total valid records available (Stage H2.2 base)** | 1892 |
| **Total unique first-visit subjects** | 1488 |
| **Repeated records excluded** | 404 |

*Note: After joining with full demographic parameters and ensuring completeness across all channels, the final deduplicated analysis pool is exactly **N = 1482** subjects.*

### Final Subject-Level Demographics

- **Female (0)**: 884 subjects
- **Male (1)**: 598 subjects
- **Age Range**: -3 to 113 (consistent with original sample definition)

The sample size change from the H2.2 record-pool (which happened to aggregate the exact same number of unique subjects via pre-median grouping in H2.2, though some individual records were repeated) is negligible in overall N, but mathematically guarantees no individual subject's test-retest covariance can inflate population PCs.
