# Compute setup

## calypso (GPU server)

- Host: `calypso` (172.18.48.182), JupyterHub (TLJH). GPU: NVIDIA A40, 48 GB.
- Haris works as `jupyter-haris` (home `/home/jupyter-haris`) through JupyterHub.
- Agents reach it over SSH from Haris's laptop as `administrator@172.18.48.182` (key auth). `administrator` has no sudo without a password and cannot write to Haris's home except where Haris granted access with an ACL.
- Work folder: `/home/jupyter-haris/graph-imputation` (clone of this repo). Created by Haris with:

  ```bash
  git clone https://github.com/harisA1/graph-imputation.git ~/graph-imputation
  setfacl -R -m u:administrator:rwX,d:u:administrator:rwX ~/graph-imputation
  ```

- Because the folder is owned by `jupyter-haris`, `administrator` has `safe.directory` set for it in its global git config (done 2026-11-12). Verified then: write access works, `import gimpute` works in the `haris` env, and the GPU is visible.

- Disk: the root filesystem was ~98% full (15 GB free) on 2026-11-12. Keep datasets small, clean up `runs/`, and ask before downloading anything large.

## Python environment: `haris`

- Path: `/opt/tljh/user/envs/haris` (Python 3.10). Also the `haris` kernel in Jupyter.
- Some packages live in Haris's user site (`~/.local`). When running as `administrator`, use:

  ```bash
  cd ~jupyter-haris/graph-imputation
  umask 002
  PYTHONUSERBASE=/home/jupyter-haris/.local /opt/tljh/user/envs/haris/bin/python -m <module>
  ```

- Present on 2026-11-12: torch 2.7.0 (CUDA 12.6, GPU visible), numpy 2.1, scipy 1.15, scikit-learn 1.7, pandas 2.2, networkx 3.4, torchmetrics, pytorch-lightning.
- **Not yet installed**, likely needed later: `torch_geometric` (and optionally `torch_scatter`/`torch_sparse` wheels for torch 2.7 + cu126), `POT` (optimal transport, for OT/GRIOT/WGNN), `pyyaml` check. Install with `pip install --user` into the `haris` env only after Haris agrees, then pin in `requirements.txt`.
