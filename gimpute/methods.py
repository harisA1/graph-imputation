"""The interface every paper implements, and how implementations are found.

A paper version lives in papers/<slug>/vN/method.py and defines one class:

    from gimpute.methods import Method, Output

    class Model(Method):
        def run(self, data, observed, seed):
            ...
            return Output(x_hat=x_hat)            # imputation methods
            # or Output(logits=logits)            # end-to-end methods
            # or both

`data.x` is the masked feature matrix (missing entries are zero), `observed` is the bool mask
[N, F] (True = known). Methods must not read ground-truth features: they never receive them.
Labels may be used only on `data.train_mask` / `data.val_mask`.

Reference baselines (no paper) live in gimpute/baselines.py and are addressed as
`--paper baseline-<name> --version v1`.
"""
from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Optional

import torch

from .data import GraphData


@dataclass
class Output:
    x_hat: Optional[torch.Tensor] = None  # [N, F] imputed features (observed entries may be anything)
    logits: Optional[torch.Tensor] = None  # [N, C] class scores, if the method classifies end to end
    extra: Optional[dict] = None  # any additional scalars to store with the results


class Method:
    """Base class. `config` is the dict loaded from the version's YAML config (may be empty)."""

    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}

    def run(self, data: GraphData, observed: torch.Tensor, seed: int) -> Output:
        raise NotImplementedError


def load_method(paper: str, version: str) -> type:
    """Return the Method subclass for a paper version."""
    if paper.startswith("baseline-"):
        from . import baselines

        try:
            return baselines.BASELINES[paper.removeprefix("baseline-")]
        except KeyError:
            raise KeyError(f"unknown baseline '{paper}'; known: {sorted(baselines.BASELINES)}") from None
    module = importlib.import_module(f"papers.{paper}.{version}.method")
    for obj in vars(module).values():
        if isinstance(obj, type) and issubclass(obj, Method) and obj is not Method and obj.__module__ == module.__name__:
            return obj
    raise ImportError(f"papers/{paper}/{version}/method.py defines no Method subclass")
