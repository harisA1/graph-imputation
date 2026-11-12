"""gimpute: shared code for the graph-imputation reimplementations.

Modules (stubs, to be implemented):
- data:      dataset loaders returning a common graph container (features, adjacency, labels, splits)
- masking:   missingness mechanisms (node attributes, edges, views) with seeded, saved masks
- metrics:   imputation metrics (RMSE, MAE, Recall@k, nDCG@k) and downstream metrics (acc, ACC/NMI/ARI)
- protocol:  the shared evaluation protocol that every paper is run through
"""

__version__ = "0.0.0"
