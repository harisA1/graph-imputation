"""FISF, version 2: version 1 with its hyper-parameters selected on the validation set."""
from gimpute.methods import load_method
from gimpute.tuning import Tuned


class FISFTuned(Tuned):
    base = load_method("um2025-propinject", "v1")
