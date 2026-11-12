# Graph imputation

A unified benchmark and reimplementation suite for **learning on graphs with missing data**: missing node attributes, incomplete structure, incomplete multi-view data, and graph-based imputation of tabular data.

Published methods in this area are evaluated on different datasets, missingness patterns, splits and metrics, which makes their numbers hard to compare. This repository reimplements them in one codebase, under one evaluation protocol, and reports how each reproduction compares with the original paper.

## Design

- **One directory per paper**, with frozen, side-by-side versions (`v1/`, `v2/`, ...) so every reported number can be regenerated.
- **One shared library** ([`gimpute/`](gimpute/)) for datasets, seeded missingness masks, metrics and the evaluation runner. Methods plug into a common interface instead of carrying their own pipeline.
- **One catalogue** ([`papers/papers.csv`](papers/papers.csv)) that drives the tables below and tracks the status of every paper.
- **Reproduction reports** in [`reports/`](reports/): our numbers against the paper's, with every deviation documented.

## Status

The shared evaluation layer, paper catalogue and reproduction-suitability assessment are in place; implementations are being added paper by paper, starting with the propagation-based baselines. See [`reports/reproduction-suitability.md`](reports/reproduction-suitability.md) for the assessment and planned order, and [`reports/log.md`](reports/log.md) for progress.

## Papers

The papers being reimplemented, grouped by problem setting. *Official code* links to the authors' repository. *Status* refers to the reimplementation in this repository. The list grows as papers are taken on.

<!-- PAPERS:START -->
### Graphs with missing node attributes

| Method | Paper | Venue | Official code | Status |
|---|---|---|---|---|
| [FP](papers/rossi2020-fp/) | On the Effectiveness of Feature Propagation in Graph Learning with Missing Node Attributes | LoG 2022 (arXiv 2021) | [twitter-research/feature-propagation](https://github.com/twitter-research/feature-propagation) | planned |
| [PaGNN](papers/jiang2021-pagnn/) | Incomplete Graph Representation and Learning via Partial Graph Neural Networks | arXiv 2021 | [yaya1015/PaGCN](https://github.com/yaya1015/PaGCN) | planned |
| [GDN](papers/li2021-deconv/) | Deconvolutional Networks on Graph Data | NeurIPS 2021 | - | planned |
| [SAGA](papers/tu2021-saga/) | Siamese Attribute-Missing Graph Auto-Encoder | arXiv 2021 | - | planned |
| [SAT](papers/chen2022-sat/) | Learning on Attribute-Missing Graphs | IEEE TPAMI 2022 | [xuChenSJTU/SAT-master-online](https://github.com/xuChenSJTU/SAT-master-online) | planned |
| [ITR](papers/tu2022-itr/) | Initializing Then Refining: A Simple Graph Attribute Imputation Network | IJCAI 2022 | [WxTu/ITR](https://github.com/WxTu/ITR) | planned |
| [MEGAE](papers/gao2023-megae/) | Handling Missing Data via Max-Entropy Regularized Graph Autoencoder | AAAI 2023 | [zqgao22/max-entropy-gae](https://github.com/zqgao22/max-entropy-gae) | planned |
| [PCFI](papers/um2023-pcfi/) | Confidence-Based Feature Imputation for Graphs with Partially Known Features | ICLR 2023 | [daehoum1/pcfi](https://github.com/daehoum1/pcfi) | planned |
| [AMGCL](papers/zhang2023-amgcl/) | Feature Imputation of Attribute-Missing Graph via Self-Supervised Contrastive Learning | arXiv 2023 | - | planned |
| [CSAT](papers/li2024-csat/) | Contrastive Sampling-Aggregating Transformer for Community Detection in Attribute-Missing Networks | IEEE TCSS 2024 | - | planned |
| [MATE](papers/peng2024-mate/) | Multi-View Graph Imputation Network | Information Fusion 2024 | [XinPeng97/MATE](https://github.com/XinPeng97/MATE) | planned |
| [GRIOT](papers/serrano2024-griot/) | Reconstructing the Unseen: GRIOT for Attributed Graph Imputation with Optimal Transport | ECML PKDD 2024 | [RichardSrn/GRIOT](https://github.com/RichardSrn/GRIOT) | planned |
| [AMGC](papers/tu2024-amgc/) | Attribute-Missing Graph Clustering Network | AAAI 2024 | [WxTu/AMGC](https://github.com/WxTu/AMGC) | planned |
| [AIAE](papers/xia2024-aiae/) | Attribute Imputation Autoencoders for Attribute-Missing Graphs | Knowledge-Based Systems 2024 | - | planned |
| [PaGC](papers/zhang2024-pagc/) | Incomplete Graph Learning via Partial Graph Convolutional Network | IEEE TAI 2024 | [yaya1015/PaGCN](https://github.com/yaya1015/PaGCN) | planned |
| [WGNN](papers/chen2025-wgnn/) | Wasserstein Graph Neural Networks for Graphs With Missing Attributes | IEEE TPAMI 2025 | - | planned |
| [DTRGC](papers/hu2025-dtrgc/) | Divide-Then-Rule: A Cluster-Driven Hierarchical Interpolator for Attribute-Missing Graphs | ACM MM 2025 | - | planned |
| [TDAR](papers/li2025-tdar/) | Topology-Driven Attribute Recovery for Attribute-Missing Graph Learning in Social Internet of Things | arXiv 2025 (IEEE IoT-J) | [limengran98/TDAR](https://github.com/limengran98/TDAR) | planned |
| [ATS](papers/liu2025-ats/) | Active Sampling for Node Attribute Completion on Graphs | arXiv 2025 | - | planned |
| [EGS](papers/song2025-egs/) | Dynamic Graph Structure Evolution for Node Classification with Missing Attributes | Scientific Reports 2025 | - | planned |
| [MV-MDCC](papers/song2025-mvmdcc/) | Multi-View Multi-Dimensional Collaborative Completion for Node Classification with Missing Attributes | Complex & Intelligent Systems 2026 | - | planned |
| [Um et al.](papers/um2025-propinject/) | Propagate and Inject: Revisiting Propagation-Based Feature Imputation for Graphs with Partially Observed Features | ICML 2025 | [daehoum1/fisf](https://github.com/daehoum1/fisf) | planned |
| [Graphiam](papers/xia2025-graphiam/) | Two-Stage Algorithm for Improving Class-Imbalanced Node Classification on Attribute-Missing Graphs | conference paper 2025 | - | planned |
| [MOBA](papers/yu2025-moba/) | Multi-View Collaborative Learning for Graph Attribute Imputation | Int. J. Machine Learning and Cybernetics 2025 | - | planned |
| [AMMGC](papers/zhao2025-ammgc/) | Attribute-Missing Multi-View Graph Clustering | CVPR 2025 | - | planned |
| [APP](papers/li2026-app/) | Adaptive Prototype-Guided Personalized Propagation for Heterophilic Graphs With Missing Data | IEEE TNNLS 2026 | [limengran98/APP](https://github.com/limengran98/APP) | planned |
| [AttriReBoost](papers/li2026-attrireboost/) | A Gradient-Free Propagation Optimization Method for Cold-Start Mitigation in Attribute-Missing Graphs | IEEE journal 2026 (arXiv 2025) | [limengran98/ARB](https://github.com/limengran98/ARB) | planned |
| [MIGDiff](papers/liu2026-migdiff/) | Multi-Attribute Imputations for Attribute-Missing Graphs via Graph Denoising Diffusion Model | AAAI 2026 | [YeLiu-Lab/MIGDiff](https://github.com/YeLiu-Lab/MIGDiff) | planned |
| [Moshiri et al.](papers/moshiri2026-iaas/) | Neighborhood-Centric Self-Supervised Graph Models for Imputation as a Service | IEEE ICWS 2026 | [erfanmoshiri/graph-imputation](https://github.com/erfanmoshiri/graph-imputation) | planned |
| [FSD-CAP](papers/qiao2026-fsdcap/) | Fractional Subgraph Diffusion with Class-Aware Propagation for Graph Feature Imputation | ICLR 2026 | [ssjcode/FSD-CAP](https://github.com/ssjcode/FSD-CAP) | planned |
| [DART](papers/song2026-dart/) | Mitigating Structural Overfitting: A Distribution-Aware Missing Feature Imputation via Two-step Reconstruction | KDD 2026 (to confirm) | [yfsong00/DART](https://github.com/yfsong00/DART) | planned |
| [WAGE](papers/tu2026-wage/) | Weight-Sharing Attribute-Missing Graph Autoencoder | IEEE TPAMI 2025 | - | planned |
| [R-AMGC](papers/wang2026-ramgc/) | Rectified Attribute-Missing Graph Clustering | under review at ICLR 2026 (anonymous) | - | planned |

### Graphs with incomplete features and structure

| Method | Paper | Venue | Official code | Status |
|---|---|---|---|---|
| [Cold Brew](papers/zheng2022-coldbrew/) | Distilling Graph Node Representations with Incomplete or Missing Neighborhoods | ICLR 2022 | [amazon-science/gnn-tail-generalization](https://github.com/amazon-science/gnn-tail-generalization) | planned |
| [UGCL](papers/fu2023-ugcl/) | Towards Unsupervised Graph Completion Learning with Feature and Structure Missing | IEEE ICDM 2023 | - | planned |
| [T2-GNN](papers/huo2023-t2gnn/) | GNNs for Graphs with Incomplete Features and Structure via Teacher-Student Distillation | AAAI 2023 | [jindi-tju/T2-GNN](https://github.com/jindi-tju/T2-GNN) | planned |
| [D2PT](papers/liu2024-d2pt/) | Learning Strong Graph Neural Networks with Weak Information | KDD 2023 | [yixinliu233/D2PT](https://github.com/yixinliu233/D2PT) | planned |
| [RITR](papers/tu2024-ritr/) | Revisiting Initializing Then Refining: An Incomplete and Missing Graph Imputation Network | IEEE TNNLS 2024 | - | planned |
| [MDS-GNN](papers/yuan2024-mdsgnn/) | Mutual Dual-Stream Graph Neural Network on Incomplete Graphs | IEEE SMC 2024 | - | planned |
| [DRI](papers/liu2025-dri/) | Incomplete Graph Learning via Data and Representation-Level Interaction | Knowledge-Based Systems 2025 | - | planned |
| [Lei et al.](papers/lei2026-weaksup/) | Training Robust Graph Completion Nets with Extremely Weak Supervision with Incomplete Features and Structure | IEEE/CAA J. Automatica Sinica 2026 | - | planned |
| [RGCN](papers/qiu2026-rgcn/) | Robust Graph Clustering Network for Multiple Missing Data | arXiv 2026 | - | planned |

### Incomplete multi-view learning

| Method | Paper | Venue | Official code | Status |
|---|---|---|---|---|
| [COMPLETER](papers/lin2021-completer/) | Incomplete Multi-View Clustering via Contrastive Prediction | CVPR 2021 | [XLearning-SCU/2021-CVPR-Completer](https://github.com/XLearning-SCU/2021-CVPR-Completer) | planned |
| [AIMC](papers/xu2021-aimc/) | Adversarial Incomplete Multiview Subspace Clustering Networks | IEEE TCYB 2022 | - | planned |
| [ACTIVE](papers/wang2022-active/) | Augmentation-Free Graph Contrastive Learning for Partial Multi-View Clustering | IJCAI 2022 | - | planned |
| [CPSPAN](papers/jin2023-cpspan/) | Deep Incomplete Multi-View Clustering with Cross-View Partial Sample and Prototype Alignment | CVPR 2023 | [jinjiaqi1998/CPSPAN](https://github.com/jinjiaqi1998/CPSPAN) | planned |
| [ProImp](papers/li2023-proimp/) | Incomplete Multi-View Clustering via Prototype-based Imputation | IJCAI 2023 | [XLearning-SCU/2023-IJCAI-ProImp](https://github.com/XLearning-SCU/2023-IJCAI-ProImp) | planned |
| [AGCL](papers/wang2023-agcl/) | Graph Contrastive Partial Multi-View Clustering | IEEE TMM 2023 | [wangemm/AGCL-TMM-2022](https://github.com/wangemm/AGCL-TMM-2022) | planned |
| [DIMvSML](papers/li2024-dimvsml/) | Deep Incomplete Multi-View Semi-Supervised Multi-Label Learning with Unbiased Loss | ACM MM 2024 (to confirm) | - | planned |
| [AGDIMC](papers/pu2024-agdimc/) | Adaptive Feature Imputation with Latent Graph for Deep Incomplete Multi-View Clustering | AAAI 2024 | - | planned |
| [DMVG](papers/wen2024-dmvg/) | Diffusion-based Missing-View Generation with the Application on Incomplete Multi-View Clustering | ICML 2024 | [Dshijie/DMVG](https://github.com/Dshijie/DMVG) | planned |
| [CSCR](papers/wang2025-cscr/) | A Category-Driven Contrastive Recovery Network for Double Incomplete Multi-View Multi-Label Classification | IEEE TMM 2025 | [wangemm/CSCR-TMM-2025](https://github.com/wangemm/CSCR-TMM-2025) | planned |
| [DCG](papers/zhang2025-dcg/) | Incomplete Multi-View Clustering via Diffusion Contrastive Generation | AAAI 2025 | [zhangyuanyang21/2025-AAAI-DCG](https://github.com/zhangyuanyang21/2025-AAAI-DCG) | planned |
| [DGGI-Net](papers/mao2026-dgginet/) | Dynamic Graph-Guided Imputation Network for Partial Multi-View Incomplete Multi-Label Classification | J. King Saud Univ. CIS 2026 | - | planned |
| [DISCM](papers/pan2026-discm/) | Diffusion-driven Incomplete Multi-View Clustering via Structured Regularization and Semantic Alignment | Multimedia Systems 2026 | - | planned |

### General data imputation

| Method | Paper | Venue | Official code | Status |
|---|---|---|---|---|
| [OT](papers/muzellec2020-ot/) | Missing Data Imputation using Optimal Transport | ICML 2020 | [BorisMuzellec/MissingDataOT](https://github.com/BorisMuzellec/MissingDataOT) | planned |
| [GINN](papers/spinelli2020-ginn/) | Missing Data Imputation with Adversarially-Trained Graph Convolutional Networks | Neural Networks 2020 | [spindro/GINN](https://github.com/spindro/GINN) | planned |
| [GRAPE](papers/you2020-grape/) | Handling Missing Data with Graph Representation Learning | NeurIPS 2020 | [maxiaoba/GRAPE](https://github.com/maxiaoba/GRAPE) | planned |
| [Wu et al.](papers/wu2023-gan-imputation/) | Differentiable and Scalable Generative Adversarial Models for Data Imputation | IEEE ICDE 2023 | - | planned |
| [Zhang et al.](papers/zhang2024-dirichlet/) | Data Imputation from the Perspective of Graph Dirichlet Energy | KDD 2024 (to confirm) | [liguanlue/GLPN](https://github.com/liguanlue/GLPN) | planned |
| [GANImputer](papers/wang2025-ganimputer/) | Generative Adversarial Learning for Missing Data Imputation | Neural Computing and Applications 2025 | [hongyuchen2andrew/GANImputer](https://github.com/hongyuchen2andrew/GANImputer) | planned |

### Fairness with missing attributes

| Method | Paper | Venue | Official code | Status |
|---|---|---|---|---|
| [FairGNN](papers/dai2022-fairgnn/) | Learning Fair GNNs with Limited and Private Sensitive Attribute Information | IEEE TKDE 2022 | [EnyanDai/FairGNN](https://github.com/EnyanDai/FairGNN) | planned |
| [FairAC](papers/guo2023-fairac/) | Fair Attribute Completion on Graph with Missing Attributes | ICLR 2023 | [donglgcn/FairAC](https://github.com/donglgcn/FairAC) | planned |
<!-- PAPERS:END -->

Candidate papers for later rounds are tracked in [`papers/INDEX.md`](papers/INDEX.md).

## Repository layout

| Path | Contents |
|---|---|
| [`papers/`](papers/) | One directory per paper (`<firstauthor><year>-<method>`): paper card, changelog, versioned implementations |
| [`papers/_template/`](papers/_template/) | Template for a new paper |
| [`gimpute/`](gimpute/) | Shared library: datasets, missingness masks, metrics, evaluation protocol |
| [`configs/`](configs/) | Shared experiment definitions (datasets, missing rates, seeds) |
| [`reports/`](reports/) | Reproduction reports and cross-paper comparisons |
| [`docs/`](docs/) | Conventions and compute setup |
| [`scripts/`](scripts/) | Catalogue and scaffolding utilities |

Datasets (`data/`) and raw run outputs (`runs/`) are not tracked. Paper PDFs are not distributed here; follow the venue links or the authors' repositories.

## Contributing

Working conventions (directory layout, versioning rules, status values) are in [`docs/conventions.md`](docs/conventions.md); the compute environment is described in [`docs/compute.md`](docs/compute.md). Automated agents should start with [`AGENTS.md`](AGENTS.md).

## Running

```bash
python tests/test_smoke.py                                   # check the shared layer (synthetic graph, CPU)
python -m gimpute.run --paper baseline-mean                  # a reference baseline over the protocol grid
python -m gimpute.run --paper <slug> --version v1            # a paper version; resumable
python -m gimpute.report                                     # rebuild reports/comparisons/leaderboard.md
```

Requires PyTorch and PyYAML; the real datasets are downloaded through PyTorch Geometric on first use.
