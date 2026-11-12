"""gimpute: the shared layer every paper reimplementation plugs into.

- data:       datasets as one GraphData container, seeded splits
- masking:    seeded missingness masks (uniform entries, structural whole-node)
- methods:    the Method interface and how paper versions are discovered
- baselines:  reference baselines (zero, mean, neighbour mean)
- downstream: the standard GCN used to score imputed features
- metrics:    imputation and classification metrics
- protocol:   evaluation of one (dataset, mechanism, rate, seed) cell
- run:        command line: run a paper version over the protocol grid, resumable
- report:     build reports/comparisons/leaderboard.md from all results
- queue:      back-to-back job queue for the single GPU
"""

__version__ = "0.1.0"
