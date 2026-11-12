# Progress log

- 2026-11-12: repository skeleton created: 63 paper directories, shared `gimpute` package stubs, conventions and compute docs. No data or implementations yet.
- 2026-11-12: all 63 papers assessed for reproduction suitability (code, open data, compute): [`reproduction-suitability.md`](reproduction-suitability.md). Official code found for 35 of 63; 22 papers in tier 1. `papers.csv` gained `code_url`, `open_data`, `repro_tier`.
- 2026-11-12: shared evaluation layer added (`gimpute/`: datasets, seeded masks, method interface, reference baselines, standard GCN, runner, leaderboard, job queue) and verified on calypso with a synthetic graph. First paper will be Feature Propagation.
- 2026-11-12: Feature Propagation reproduced ([report](rossi2020-fp.md)). The shared protocol now follows the FP setting (largest connected component, FP classifier settings). PCFI v1 implemented and running.
- 2026-11-12: PCFI v1 and FISF v1 (authors' default settings) run on the full grid with the three reference baselines; first [leaderboard](comparisons/leaderboard.md). Both partially reproduce their papers ([PCFI](um2023-pcfi.md), [FISF](um2025-propinject.md)); validation-tuned v2 versions are next. Missing rate 0.995 added to the protocol.
