"""Hyper-parameter selection on the validation set, for methods whose papers tune per dataset.

A tuned version wraps an existing version:

    from gimpute.methods import load_method
    from gimpute.tuning import Tuned

    class Model(Tuned):
        base = load_method("um2023-pcfi", "v1")

and its config lists the grid (every other key is passed to the base method unchanged):

    grid:
      alpha: [0.1, 0.5, 0.9]
      beta: [0.000001, 1.0]
    tie:            # optional: parameters that copy another one instead of being searched
      beta: alpha

For every combination the base method imputes the features, the standard GCN is trained on them
with the protocol's settings, and the combination with the best validation accuracy is returned.
Only training and validation labels are used; the test nodes play no part in the choice.
"""
from __future__ import annotations

import itertools

import torch

from .downstream import train_gcn
from .methods import Method, Output


class Tuned(Method):
    base: type = None  # the Method subclass to tune

    def run(self, data, observed, seed):
        grid = self.config.get("grid", {})
        tie = self.config.get("tie", {})
        fixed = {k: v for k, v in self.config.items() if k not in ("grid", "tie")}
        downstream = self.protocol.get("downstream", {})
        best = None
        for values in itertools.product(*grid.values()):
            params = dict(zip(grid.keys(), values))
            params.update({k: params[src] for k, src in tie.items()})
            out = self.base({**fixed, **params}).run(data, observed, seed)
            x_hat = torch.where(observed, data.x, out.x_hat)
            val = train_gcn(data, x_hat, seed, **downstream)["val_acc"]
            if best is None or val > best[0]:
                best = (val, params, out.x_hat)
        val, params, x_hat = best
        extra = {f"tuned_{k}": v for k, v in params.items()}
        extra["tuning_val_acc"] = val
        extra["tuning_candidates"] = len(list(itertools.product(*grid.values())))
        return Output(x_hat=x_hat, extra=extra)
