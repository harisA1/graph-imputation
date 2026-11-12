"""<METHOD> (<paper slug>), version 1. Follows the paper as closely as possible."""
from gimpute.methods import Method, Output


class Model(Method):
    def run(self, data, observed, seed):
        # data.x: masked features (missing = 0); observed: bool [N, F], True = known.
        # Return Output(x_hat=...) for imputation, Output(logits=...) for end-to-end methods, or both.
        raise NotImplementedError
