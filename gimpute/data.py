"""Datasets. Everything is returned as a `GraphData`, whatever library it came from.

Real datasets are downloaded to data/ (git-ignored) through torch_geometric, imported lazily
so that the rest of the package works without it. `sbm` is a small synthetic graph for tests.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Callable, Dict

import torch

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


@dataclass
class GraphData:
    name: str
    x: torch.Tensor  # [N, F] float features (ground truth; methods receive a masked copy)
    edge_index: torch.Tensor  # [2, E] long, undirected (both directions present)
    y: torch.Tensor  # [N] long labels
    num_classes: int
    train_mask: torch.Tensor  # [N] bool
    val_mask: torch.Tensor
    test_mask: torch.Tensor

    @property
    def num_nodes(self) -> int:
        return self.x.shape[0]

    @property
    def binary_features(self) -> bool:
        return bool(((self.x == 0) | (self.x == 1)).all())

    def to(self, device) -> "GraphData":
        return replace(self, **{k: v.to(device) for k, v in self.__dict__.items() if torch.is_tensor(v)})

    def with_features(self, x: torch.Tensor) -> "GraphData":
        return replace(self, x=x)

    def with_split(self, train, val, test) -> "GraphData":
        return replace(self, train_mask=train, val_mask=val, test_mask=test)


def random_split(y: torch.Tensor, seed: int, train_per_class: int = 20, num_val: int = 1500):
    """Seeded split: `train_per_class` nodes per class, `num_val` validation nodes, rest test.
    On small graphs the sizes shrink so that at least a third of the nodes stay in test."""
    g = torch.Generator().manual_seed(seed)
    n = y.numel()
    classes = y.unique()
    train_per_class = max(1, min(train_per_class, n // (6 * len(classes))))
    num_val = min(num_val, n // 3)
    train = torch.zeros(n, dtype=torch.bool)
    for c in classes:
        idx = (y == c).nonzero().squeeze(1)
        train[idx[torch.randperm(idx.numel(), generator=g)[:train_per_class]]] = True
    rest = (~train).nonzero().squeeze(1)
    rest = rest[torch.randperm(rest.numel(), generator=g)]
    val = torch.zeros(n, dtype=torch.bool)
    val[rest[:num_val]] = True
    test = torch.zeros(n, dtype=torch.bool)
    test[rest[num_val:]] = True
    return train, val, test


def _to_undirected(edge_index: torch.Tensor, n: int) -> torch.Tensor:
    ei = torch.cat([edge_index, edge_index.flip(0)], dim=1)
    ei = ei[:, ei[0] != ei[1]]
    key = torch.unique(ei[0] * n + ei[1])
    return torch.stack([key // n, key % n])


def _sbm(n: int = 600, classes: int = 4, feats: int = 32, p_in: float = 0.05, p_out: float = 0.005, seed: int = 0):
    g = torch.Generator().manual_seed(seed)
    y = torch.arange(n) % classes
    prob = torch.where(y[:, None] == y[None, :], p_in, p_out)
    adj = torch.rand(n, n, generator=g) < prob
    edge_index = _to_undirected(torch.triu(adj, 1).nonzero().t(), n)
    centers = torch.randn(classes, feats, generator=g)
    x = centers[y] + 0.8 * torch.randn(n, feats, generator=g)
    empty = torch.zeros(n, dtype=torch.bool)
    return GraphData("sbm", x, edge_index, y, classes, empty, empty, empty)


def _pyg(cls_name: str, name: str | None) -> Callable[[], GraphData]:
    def load() -> GraphData:
        import torch_geometric.datasets as D  # lazy: only needed for real datasets

        root = str(DATA_DIR / cls_name.lower())
        ds = getattr(D, cls_name)(root, name) if name else getattr(D, cls_name)(root)
        d = ds[0]
        n = d.num_nodes
        empty = torch.zeros(n, dtype=torch.bool)
        return GraphData(
            (name or cls_name).lower(), d.x.float(), _to_undirected(d.edge_index, n), d.y.long(),
            int(d.y.max()) + 1, empty, empty, empty,
        )

    return load


DATASETS: Dict[str, Callable[[], GraphData]] = {
    "sbm": _sbm,
    "cora": _pyg("Planetoid", "Cora"),
    "citeseer": _pyg("Planetoid", "CiteSeer"),
    "pubmed": _pyg("Planetoid", "PubMed"),
    "photo": _pyg("Amazon", "Photo"),
    "computers": _pyg("Amazon", "Computers"),
    "cs": _pyg("Coauthor", "CS"),
    "physics": _pyg("Coauthor", "Physics"),
}


def load_dataset(name: str, split_seed: int = 0) -> GraphData:
    """Load a dataset and attach a seeded random split (same seed -> same split for every method)."""
    if name not in DATASETS:
        raise KeyError(f"unknown dataset '{name}'; known: {sorted(DATASETS)}")
    data = DATASETS[name]()
    return data.with_split(*random_split(data.y, split_seed))
