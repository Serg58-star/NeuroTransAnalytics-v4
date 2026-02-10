---
name: no-real-data-until-approved
description: Prevents the use of real data sources (SQLite, CSV, Excel, etc.) until explicit approval. Triggers on database or file-loading attempts.
---

# No Real Data Until Approved

This skill prevents premature coupling of exploratory procedures
to real datasets.

## When to use this skill
- When code references data loading.
- When database connections are mentioned.
- When file I/O is introduced.

## Prohibited Until Explicit Approval

- SQLite connections.
- Reading CSV, Excel, or MDB files.
- Loading real experimental data.
- ETL pipelines.

## Allowed

- Synthetic data generation.
- Mock data.
- Randomized or parametric test datasets.

## Trigger Keywords

- sqlite
- database
- db
- connect
- load
- read_csv
- read_excel

## Enforcement

If real data access is detected:
- STOP immediately.
- Report the attempted violation.
- Await explicit user approval.

This skill protects methodological purity.
