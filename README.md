# Graph imputation

Reimplementations of methods for learning and imputation on graphs (and related data) with missing values: missing node attributes, missing structure, incomplete multi-view data, and graph-based tabular imputation.

The aim is one comparable codebase: every paper gets its own directory, shares the same data loaders, masking protocols and metrics, and keeps every version of its implementation so results stay reproducible.

**Status:** skeleton only. No datasets and no implementations yet. See [`papers/INDEX.md`](papers/INDEX.md) for the 63 papers and their status.

## Layout

| Path | What lives there |
|---|---|
| [`papers/`](papers/) | One directory per paper (`<firstauthor><year>-<method>`), each with versioned implementations `v1/`, `v2/`, ... |
| [`papers/papers.csv`](papers/papers.csv) | Machine-readable catalogue: the source of truth for slugs, categories, priority and status |
| [`papers/_template/`](papers/_template/) | Copy this to start a new paper |
| [`gimpute/`](gimpute/) | Shared Python package: datasets, missingness masks, metrics, evaluation protocol |
| [`configs/`](configs/) | Shared experiment configs (datasets, missing rates, seeds) |
| [`reports/`](reports/) | Human-readable reports: per-paper reproduction reports and cross-paper comparisons |
| [`docs/`](docs/) | Conventions, compute setup, design notes |
| [`scripts/`](scripts/) | Utility scripts (scaffolding, index generation) |
| `data/`, `runs/` | Local only, git-ignored: datasets and raw run outputs |

## Paper categories

| Code | Category |
|---|---|
| A | Graphs with missing node attributes (feature imputation / attribute completion) |
| B | Graphs with incomplete features **and** structure (or weak labels) |
| C | Incomplete multi-view learning (clustering / classification) |
| D | General (tabular) data imputation, incl. graph-, OT- and GAN-based |
| E | Fairness with missing attributes |

## Where things run

Development happens on Haris's laptop; training runs on the `calypso` GPU server (NVIDIA A40) in `~/graph-imputation` with the `haris` conda environment. See [`docs/compute.md`](docs/compute.md).

## For agents

Start with [`AGENTS.md`](AGENTS.md).

## Note on papers

The paper PDFs are not in this repository. They are kept privately; `papers.csv` records each paper's filename so it can be matched.
