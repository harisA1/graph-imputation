# Changelog

One entry per version. A version is frozen once its results appear in `reports/`; changes that can alter results go into a new version.

## v2 (2026-11-12)

- v1 with its hyper-parameters selected on the validation set (`gimpute/tuning.py`), as the paper does. Grid in `v2/configs/default.yaml`.
- Run at 99.5% missing, 10 seeds. Reproduces the paper's headline table.

## v1 (2026-11-12)

- First implementation, following the paper and checked against the authors' code, with the code's default hyper-parameters. All feature channels are processed at once.
- Run on the full protocol grid, 10 seeds.
