"""Reproduce Table 1 of the paper under the authors' own split.

    python -m papers.rossi2020-fp.v1.paper_setting

The shared protocol draws a new train/validation/test split for every seed. The authors' code
instead fixes one "development" set of 1500 nodes (seed 1684992425); every run takes its
20-per-class training nodes from it, validates on the rest of it, and tests on all other nodes,
so the test set is the same in every run. On small graphs (CiteSeer's largest component has
2120 nodes, so 620 test nodes) that single test set moves the mean by several points, which
is why this setting is needed to compare with the paper's numbers.

The split logic and the seed constants below are taken from the authors' repository
(twitter-research/feature-propagation, Apache-2.0). Results go to results/paper_setting.jsonl.
"""
import json
from pathlib import Path

import numpy as np
import torch
import yaml

from gimpute.data import _load
from gimpute.downstream import train_gcn
from gimpute.masking import apply_mask, make_mask
from gimpute.methods import load_method
from gimpute.run import ROOT, git_commit

DEVELOPMENT_SEED = 1684992425
RUN_SEEDS = [4258031807, 3829679737, 3706579387, 789594926, 3628091752,
             54121625, 825346923, 646393804, 1579300575, 246132812]
DATASETS = ["cora", "citeseer", "pubmed", "photo", "computers"]
RATES = [0.0, 0.5, 0.9, 0.99]
OUT = Path(__file__).parent / "results" / "paper_setting.jsonl"


def authors_split(data, seed: int):
    n, y = data.num_nodes, data.y.numpy()
    development = np.random.RandomState(DEVELOPMENT_SEED).choice(n, 1500, replace=False)
    rnd = np.random.RandomState(seed)
    train = []
    for c in range(int(y.max()) + 1):
        train.extend(rnd.choice(development[np.where(y[development] == c)[0]], 20, replace=False))

    def mask(idx):
        m = torch.zeros(n, dtype=torch.bool)
        m[torch.as_tensor(np.asarray(idx))] = True
        return m

    train_mask, dev_mask = mask(train), mask(development)
    return data.with_split(train_mask, dev_mask & ~train_mask, ~dev_mask)


def main() -> None:
    proto = yaml.safe_load((ROOT / "configs" / "protocol.yaml").read_text(encoding="utf-8"))
    config = yaml.safe_load((Path(__file__).parent / "configs" / "default.yaml").read_text(encoding="utf-8"))
    method = load_method("rossi2020-fp", "v1")(config)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    done = set()
    if OUT.exists():
        done = {(r["dataset"], r["rate"], r["run"]) for r in map(json.loads, OUT.read_text().splitlines())}
    commit = git_commit()
    for dataset in DATASETS:
        base = _load(dataset, True)  # largest connected component, as in the authors' code
        for rate in RATES:
            for run, seed in enumerate(RUN_SEEDS):
                if (dataset, rate, run) in done:
                    continue
                data = authors_split(base, seed)
                observed = make_mask(data.num_nodes, data.x.shape[1], "uniform", rate, run).to(device)
                masked = data.with_features(apply_mask(data.x, observed.cpu())).to(device)
                x_hat = torch.where(observed, masked.x, method.run(masked, observed, run).x_hat)
                row = {"dataset": dataset, "rate": rate, "run": run, "split_seed": seed,
                       **train_gcn(masked, x_hat, run, **proto["downstream"]), "commit": commit}
                with open(OUT, "a", encoding="utf-8") as f:
                    f.write(json.dumps(row) + "\n")
            print(dataset, rate, "done", flush=True)


if __name__ == "__main__":
    main()
