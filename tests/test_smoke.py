"""End-to-end check of the shared layer on the synthetic graph (no downloads, runs on CPU).

    python tests/test_smoke.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch

from gimpute import metrics
from gimpute.data import load_dataset
from gimpute.masking import make_mask
from gimpute.methods import load_method
from gimpute.protocol import evaluate_cell


def test_masks():
    a = make_mask(100, 20, "uniform", 0.7, seed=3)
    assert torch.equal(a, make_mask(100, 20, "uniform", 0.7, seed=3)), "masks must be deterministic"
    assert abs((~a).float().mean().item() - 0.7) < 0.05
    s = make_mask(100, 20, "structural", 0.6, seed=3)
    assert (~s).all(1).sum().item() == 60 and (s.all(1) | (~s).all(1)).all()


def test_split():
    d = load_dataset("sbm", split_seed=1)
    assert not (d.train_mask & d.val_mask).any() and not (d.train_mask & d.test_mask).any() and not (d.val_mask & d.test_mask).any()
    assert (d.train_mask | d.val_mask | d.test_mask).all()
    assert torch.equal(d.train_mask, load_dataset("sbm", split_seed=1).train_mask)


def test_metrics():
    x = torch.tensor([[1.0, 0.0, 1.0, 0.0]])
    obs = torch.zeros(1, 4, dtype=torch.bool)
    assert metrics.rmse(x, x, obs) == 0.0
    r, n = metrics.recall_ndcg_at_k(torch.tensor([[0.9, 0.1, 0.8, 0.2]]), x, obs, k=2)
    assert abs(r - 1.0) < 1e-6 and abs(n - 1.0) < 1e-6
    r, _ = metrics.recall_ndcg_at_k(torch.tensor([[0.1, 0.9, 0.2, 0.8]]), x, obs, k=2)
    assert r == 0.0


def test_pipeline():
    res = {}
    for name in ("zero", "mean", "neighbor-mean"):
        method = load_method(f"baseline-{name}", "v1")()
        res[name] = evaluate_cell(method, "sbm", "uniform", 0.8, seed=0, device="cpu")
        assert 0.0 <= res[name]["test_acc"] <= 1.0
    assert res["mean"]["rmse"] < res["zero"]["rmse"], res
    assert res["neighbor-mean"]["rmse"] < res["mean"]["rmse"], res
    assert res["neighbor-mean"]["test_acc"] > 0.5, res
    s = evaluate_cell(load_method("baseline-neighbor-mean", "v1")(), "sbm", "structural", 0.5, seed=0, device="cpu")
    assert s["rmse"] == s["rmse"]


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
