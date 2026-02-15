# Dependency Notes — Parquet Stability

## Context

Initial implementations of the C3 Layer (v4) utilized `pyarrow` as the default engine for Parquet persistence. In the current development environment (Windows, Python 3.13.5), `pyarrow 19.0.0` exhibited critical instability:

- Silent crashes during `pd.read_parquet` and `pq.read_table`.
- Process hang on read operations regardless of thread settings.

## Decision: Shift to fastparquet

To ensure architectural integrity and system stability, the project has shifted to `fastparquet` for all Parquet operations.

### Frozen Versions

- `fastparquet==2025.12.0`
- `cramjam==2.11.0`

### Rationale

`fastparquet` is a pure-python implementation with C/Rust extensions (cramjam) that proved stable and efficient in our environment during diagnostic testing. It avoids the native memory access issues encountered with the current `pyarrow` build on Windows/Py3.13.

### Implementation Pattern

All Parquet operations must explicitly specify the engine:

```python
df.to_parquet(path, engine="fastparquet", index=False)
df = pd.read_parquet(path, engine="fastparquet")
```
