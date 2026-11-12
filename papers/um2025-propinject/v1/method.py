"""FISF: feature imputation with synthetic features (Um et al., "Propagate and Inject",
ICML 2025), version 1. No trainable parameters.

Propagation-based imputation leaves some channels almost constant over the graph (for example
when a channel has very few observed values), and such channels carry no information for the
downstream model. FISF repairs them:

1. Pre-diffusion: PCFI's confidence-weighted diffusion on every channel.
2. Take the fraction gamma of channels with the lowest variance after pre-diffusion.
3. Inject: in each of those channels, give one randomly chosen node a random value in [0, 1)
   and treat it as observed.
4. Diffuse those channels again with a combined pseudo-confidence alpha^S * beta^V, where S is
   the distance to the nearest observed node and V the distance to the injected node, so the
   synthetic value spreads over the whole graph and breaks the constant channel. The other
   channels keep their pre-diffusion result.

Follows the authors' code (github.com/daehoum1/fisf, Apache-2.0), including a detail that
differs between the missingness types there: under structural missingness S ignores the
injected node, under uniform missingness it includes it.
"""
import torch

from gimpute.methods import Method, Output
from gimpute.propagation import adjacency_with_self_loops, confidence_diffusion, distance_to_observed


class FISF(Method):
    def run(self, data, observed, seed):
        alpha = float(self.config.get("alpha", 0.9))
        beta = float(self.config.get("beta", 0.9))
        gamma = float(self.config.get("gamma", 0.7))
        iters = int(self.config.get("num_iterations", 100))
        n, f = data.x.shape
        dev = data.x.device
        adj = adjacency_with_self_loops(data.edge_index, n)

        # 1. pre-diffusion
        dist = distance_to_observed(adj, observed)
        x = confidence_diffusion(adj, data.x, observed, alpha ** dist, iters)

        # 2. low-variance channels
        num_low = int(f * gamma)
        if num_low == 0:
            return Output(x_hat=x)
        low = torch.topk(x.var(dim=0), num_low, largest=False).indices

        # 3. inject one synthetic value per low-variance channel
        g = torch.Generator().manual_seed(seed)
        nodes = torch.randint(n, (num_low,), generator=g).to(dev)
        values = torch.rand(num_low, generator=g).to(dev)
        cols = torch.arange(num_low, device=dev)
        known_low = data.x[:, low].clone()
        observed_low = observed[:, low].clone()
        known_low[nodes, cols] = values
        observed_low[nodes, cols] = True
        injected = torch.zeros(n, num_low, dtype=torch.bool, device=dev)
        injected[nodes, cols] = True

        # 4. re-diffuse the low-variance channels with the combined pseudo-confidence
        structural = bool((observed.all(dim=1) | (~observed).all(dim=1)).all())
        dist_low = dist[:, low] if structural else distance_to_observed(adj, observed_low)
        conf = (alpha ** dist_low) * (beta ** distance_to_observed(adj, injected))
        x[:, low] = confidence_diffusion(adj, known_low, observed_low, conf, iters)
        return Output(x_hat=x, extra={"low_variance_channels": num_low})
