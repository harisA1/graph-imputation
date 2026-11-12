# Graph imputation

A unified benchmark and reimplementation suite for **learning on graphs with missing data**: missing node attributes, incomplete structure, incomplete multi-view data, and graph-based imputation of tabular data.

Published methods in this area are evaluated on different datasets, missingness patterns, splits and metrics, which makes their numbers hard to compare. This repository reimplements them in one codebase, under one evaluation protocol, and reports how each reproduction compares with the original paper.

## Design

- **One directory per paper**, with frozen, side-by-side versions (`v1/`, `v2/`, ...) so every reported number can be regenerated.
- **One shared library** ([`gimpute/`](gimpute/)) for datasets, seeded missingness masks, metrics and the evaluation runner. Methods plug into a common interface instead of carrying their own pipeline.
- **One catalogue** ([`papers/papers.csv`](papers/papers.csv)) that drives the tables below and tracks the status of every paper.
- **Reproduction reports** in [`reports/`](reports/): our numbers against the paper's, with every deviation documented.

## Status

The shared evaluation layer, paper catalogue and reproduction-suitability assessment are in place; implementations are being added paper by paper, starting with the propagation-based baselines. See [`reports/reproduction-suitability.md`](reports/reproduction-suitability.md) for the assessment and planned order, and [`reports/log.md`](reports/log.md) for progress.

## Papers

The papers being reimplemented, grouped by problem setting. *Official code* links to the authors' repository. *Status* refers to the reimplementation in this repository. The list grows as papers are taken on.

<!-- PAPERS:START -->
### Graphs with missing node attributes

| Method | Paper | Venue | Official code | Status |
|---|---|---|---|---|
| [FP](papers/rossi2020-fp/) | On the Unreasonable Effectiveness of Feature Propagation in Learning on Graphs with Missing Node Features | LoG 2022 (arXiv 2021) | [twitter-research/feature-propagation](https://github.com/twitter-research/feature-propagation) | reproduced |
| [SAT](papers/chen2022-sat/) | Learning on Attribute-Missing Graphs | IEEE TPAMI 2022 | [xuChenSJTU/SAT-master-online](https://github.com/xuChenSJTU/SAT-master-online) | up next |
| [PCFI](papers/um2023-pcfi/) | Confidence-Based Feature Imputation for Graphs with Partially Known Features | ICLR 2023 | [daehoum1/pcfi](https://github.com/daehoum1/pcfi) | in progress |
| [FISF](papers/um2025-propinject/) | Propagate and Inject: Revisiting Propagation-Based Feature Imputation for Graphs with Partially Observed Features | ICML 2025 | [daehoum1/fisf](https://github.com/daehoum1/fisf) | up next |
<!-- PAPERS:END -->

Candidate papers for later rounds are tracked in [`papers/INDEX.md`](papers/INDEX.md).

## Repository layout

| Path | Contents |
|---|---|
| [`papers/`](papers/) | One directory per paper (`<firstauthor><year>-<method>`): paper card, changelog, versioned implementations |
| [`papers/_template/`](papers/_template/) | Template for a new paper |
| [`gimpute/`](gimpute/) | Shared library: datasets, missingness masks, metrics, evaluation protocol |
| [`configs/`](configs/) | Shared experiment definitions (datasets, missing rates, seeds) |
| [`reports/`](reports/) | Reproduction reports and cross-paper comparisons |
| [`docs/`](docs/) | Conventions and compute setup |
| [`scripts/`](scripts/) | Catalogue and scaffolding utilities |

Datasets (`data/`) and raw run outputs (`runs/`) are not tracked. Paper PDFs are not distributed here; follow the venue links or the authors' repositories.

## Contributing

Working conventions (directory layout, versioning rules, status values) are in [`docs/conventions.md`](docs/conventions.md); the compute environment is described in [`docs/compute.md`](docs/compute.md). Automated agents should start with [`AGENTS.md`](AGENTS.md).

## Running

```bash
python tests/test_smoke.py                                   # check the shared layer (synthetic graph, CPU)
python -m gimpute.run --paper baseline-mean                  # a reference baseline over the protocol grid
python -m gimpute.run --paper <slug> --version v1            # a paper version; resumable
python -m gimpute.report                                     # rebuild reports/comparisons/leaderboard.md
```

Requires PyTorch and PyYAML; the real datasets are downloaded through PyTorch Geometric on first use.

## License

[MIT](LICENSE). Each reimplemented method remains the work of its original authors; please cite the original papers.
