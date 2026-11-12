"""Missingness mechanisms. A mask is a bool tensor [N, F], True = observed.

Masks depend only on (shape, mechanism, rate, seed), so every method sees identical missing entries.

- uniform:    each entry is missing independently with probability `rate`
              ("partially missing features"; FP, PCFI, ...).
- structural: a fraction `rate` of nodes lose all their features
              ("attribute-missing graphs"; SAT, ITR, ...).
"""
from __future__ import annotations

import torch

MECHANISMS = ("uniform", "structural")


def make_mask(num_nodes: int, num_features: int, mechanism: str, rate: float, seed: int) -> torch.Tensor:
    if not 0.0 <= rate < 1.0:
        raise ValueError("rate must be in [0, 1)")
    g = torch.Generator().manual_seed(seed)
    if mechanism == "uniform":
        return torch.rand(num_nodes, num_features, generator=g) >= rate
    if mechanism == "structural":
        missing = torch.randperm(num_nodes, generator=g)[: int(round(rate * num_nodes))]
        observed = torch.ones(num_nodes, dtype=torch.bool)
        observed[missing] = False
        return observed[:, None].expand(num_nodes, num_features).clone()
    raise ValueError(f"unknown mechanism '{mechanism}'; known: {MECHANISMS}")


def apply_mask(x: torch.Tensor, observed: torch.Tensor) -> torch.Tensor:
    """Features as a method sees them: missing entries set to zero."""
    return torch.where(observed, x, torch.zeros_like(x))
