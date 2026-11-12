"""PCFI, version 2: version 1 with alpha and beta selected on the validation set, as in the paper."""
from gimpute.methods import load_method
from gimpute.tuning import Tuned


class PCFITuned(Tuned):
    base = load_method("um2023-pcfi", "v1")
