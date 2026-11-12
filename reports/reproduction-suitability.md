# Which papers are suitable for reproduction

Assessed 2026-11-12 from the 63 PDFs in `SELECTED/`. Per-paper detail is in each `papers/<slug>/README.md`; the machine-readable columns are `code_url`, `open_data` and `repro_tier` in [`papers/papers.csv`](../papers/papers.csv).

## Summary

- **Data is not the bottleneck.** All 63 papers evaluate on public datasets. Three also report on data that cannot be obtained (Cold Brew's proprietary e-commerce sets, Moshiri's 6M-node property graph) or that is too large to be worth it here (Wu 2023's million-row tables), and only their public tables can be reproduced.
- **Code is the bottleneck.** An official repository was found for 35 of 63 papers. The other 28 would have to be rebuilt from the text.
- **Compute is not a constraint** for almost everything: the graph papers use Cora, Citeseer, PubMed, Amazon Photo/Computers and at most ogbn-arxiv, which train in minutes on the A40 and need well under 1 GB of disk. Exceptions are listed under *Compute and disk*.
- Tiers: 22 in tier 1, 14 in tier 2, 25 in tier 3, 2 in tier 4.

## How the tiers were decided

| Tier | Meaning |
|---|---|
| 1 | Official code found, public data, cheap to run, and central enough to be worth it. Start here. |
| 2 | Reproducible, with a caveat: part of the data is private, the repo looks thin or unlicensed, the experiments are heavy, or the topic is at the edge of the project. |
| 3 | Public data but no official code found. Must be reimplemented from the paper, so matching the reported numbers is uncertain. |
| 4 | Defer: unpublished, or poor fit for the project and the server. |

Criteria checked for every paper: (1) official code, by reading the PDF for a link and searching GitHub; (2) whether the datasets are public and how large; (3) hardware reported and method cost; (4) venue and whether later papers in this collection use it as a baseline; (5) Haris's priority marker.

**Limits of this assessment.** Repositories were confirmed to exist and to be non-empty (size, language, last push), but none has been cloned or run yet. 'None found' means a GitHub search by method name, title words and author account returned nothing; code may still exist on a personal page or be available on request. Venues marked 'to confirm' were not stated in the PDF. Dataset lists come from a text scan of each PDF and name the main benchmarks, not necessarily every dataset in the appendix; confirm against the paper when filling in the paper card.

## Recommended order

1. **Propagation baselines** (hours, no training to speak of): FP, PCFI, Propagate-and-Inject (FISF), AttriReBoost, PaGNN/PaGC. These give the shared protocol for *partially missing* features.
2. **Attribute-missing (whole nodes without features)**: SAT, then ITR, MATE, TDAR, AMGC. They share one protocol (Recall@k, nDCG@k, classification, clustering).
3. **Priority-5 papers with code**: GRIOT, MIGDiff, AGCL. Also FSD-CAP and DART as the two newest strong-venue methods with code.
4. **Features and structure both incomplete**: T2-GNN and D2PT (both with code and released data), then RITR on top of ITR.
5. **Tabular baselines** needed by the OT and graph-of-table methods: OT (Muzellec), GRAPE, GINN, GLPN.
6. **Multi-view**, if kept in scope: COMPLETER, then ProImp, DCG, AGCL.
7. Tier 3 papers only after their nearest tier-1 relative runs (for example EWS-RGCN after D2PT, ATS after SAT, WAGE after ITR, ACTIVE after AGCL, DTRGC after AMGC).

Priority-5 papers without code (DTRGC, Lei 2026 EWS-RGCN, ACTIVE) are the ones where a decision is needed: reimplement from the paper, or write to the authors first.

## Tier 1 - start here

| Paper | Year | Cat. | Prio | Venue | Official code | Data | Notes |
|---|---|---|---|---|---|---|---|
| [GRIOT](../papers/serrano2024-griot/) | 2024 | A | 5 | ECML PKDD 2024 | [RichardSrn/GRIOT](https://github.com/RichardSrn/GRIOT) | Cora, CiteSeer, PubMed variants, WikiCS-type graphs, synthetic SBM | Priority 5, official code, public data. Needs POT. OT cost is quadratic in nodes, so PubMed-size runs are slow; the repo is ~130 MB. |
| [MIGDiff](../papers/liu2026-migdiff/) | 2026 | A | 5 | AAAI 2026 | [YeLiu-Lab/MIGDiff](https://github.com/YeLiu-Lab/MIGDiff) | Cora, Citeseer, Amazon-Computers, Amazon-Photo | Priority 5, official code, small graphs. Diffusion sampling makes it slower than the propagation methods but well within one A40. |
| [FP](../papers/rossi2020-fp/) | 2020 | A | 4 | LoG 2022 (arXiv 2021) | [twitter-research/feature-propagation](https://github.com/twitter-research/feature-propagation) | Cora, CiteSeer, PubMed, Photo, Computers, OGBN-Arxiv, OGBN-Products | The canonical baseline; almost every later paper compares with it. Trivial compute. Skip OGBN-Products/papers100M at first (large downloads). |
| [SAT](../papers/chen2022-sat/) | 2022 | A | 4 | IEEE TPAMI 2022 | [xuChenSJTU/SAT-master-online](https://github.com/xuChenSJTU/SAT-master-online) | Cora, Citeseer, PubMed, Steam, Amazon-Computers/Photo, Coauthor-CS | The reference setting for attribute-missing graphs (Recall@k / nDCG@k profiling plus node classification). Its protocol is reused by ITR, SVGA, MATE, TDAR and others, so reproducing it first fixes the shared protocol. |
| [ITR](../papers/tu2022-itr/) | 2022 | A | 4 | IJCAI 2022 | [WxTu/ITR](https://github.com/WxTu/ITR) | Cora, Citeseer, Amazon-Computers, Amazon-Photo | Official code (Apache-2.0), short paper, widely used baseline. |
| [MATE](../papers/peng2024-mate/) | 2024 | A | 4 | Information Fusion 2024 | [XinPeng97/MATE](https://github.com/XinPeng97/MATE) | Cora, Citeseer, Amazon-Computers, Amazon-Photo | Official code (Apache-2.0), same protocol family as ITR. |
| [AMGC](../papers/tu2024-amgc/) | 2024 | A | 4 | AAAI 2024 | [WxTu/AMGC](https://github.com/WxTu/AMGC) | Cora, Citeseer, Amazon-Photo, and similar | Official code. The reference for clustering on attribute-missing graphs (baseline for DTRGC, R-AMGC, AMMGC). |
| [TDAR](../papers/li2025-tdar/) | 2025 | A | 4 | arXiv 2025 (IEEE IoT-J) | [limengran98/TDAR](https://github.com/limengran98/TDAR) | Cora, Citeseer, PubMed, Amazon-Computers, Amazon-Photo, CS | Official PyTorch code (MIT), SAT-style protocol, cheap. |
| [um2025-propinject](../papers/um2025-propinject/) | 2025 | A | 4 | ICML 2025 | [daehoum1/fisf](https://github.com/daehoum1/fisf) | Cora, CiteSeer, PubMed, Photo, Computers, OGBN-Arxiv, synthetic | Official code (FISF, Apache-2.0). Natural follow-up to PCFI; do the two together. |
| [AttriReBoost](../papers/li2026-attrireboost/) | 2026 | A | 4 | IEEE journal 2026 (arXiv 2025) | [limengran98/ARB](https://github.com/limengran98/ARB) | Cora, CiteSeer, PubMed, Computers, Photo, CS, ogbn-arxiv | Gradient-free propagation (paper reports seconds per run). Tiny official repo. One of the cheapest papers in the set. |
| [FSD-CAP](../papers/qiao2026-fsdcap/) | 2026 | A | 4 | ICLR 2026 | [ssjcode/FSD-CAP](https://github.com/ssjcode/FSD-CAP) | Cora, CiteSeer, PubMed, Photo, Computers, heterophilic sets, ogbn-arxiv (all via PyG) | Official code with seeds. Recent and strong venue; compares against FP, PCFI, PaGCN, ITR, so it doubles as a check of our baselines. |
| [DART](../papers/song2026-dart/) | 2026 | A | 4 | KDD 2026 (to confirm) | [yfsong00/DART](https://github.com/yfsong00/DART) | Cora, Citeseer, PubMed, ogbn-arxiv, Flickr, Reddit, and their new Sailing dataset | Official code and data (MIT). Reddit is the only larger set (a few GB); the rest is small. Introduces a dataset with naturally missing features. |
| [PCFI](../papers/um2023-pcfi/) | 2023 | A | 3 | ICLR 2023 | [daehoum1/pcfi](https://github.com/daehoum1/pcfi) | Cora, CiteSeer, PubMed, Photo, Computers, OGBN-Arxiv (PyG) | Official code (Apache-2.0), tiny, propagation-based. Priority 3 by marker, but it is a standard baseline and nearly free to run. |
| [T2-GNN](../papers/huo2023-t2gnn/) | 2023 | B | 4 | AAAI 2023 | [jindi-tju/T2-GNN](https://github.com/jindi-tju/T2-GNN) | Cora, Citeseer, Squirrel, Chameleon, Texas, Cornell, Wisconsin (data.zip in repo) | Official code with the exact data and missing masks. The data split is reused by DRI and others. |
| [D2PT](../papers/liu2024-d2pt/) | 2024 | B | 4 | KDD 2023 | [yixinliu233/D2PT](https://github.com/yixinliu233/D2PT) | Cora, CiteSeer, PubMed, Amazon, Coauthor, ogbn-arxiv (8 public sets) | Official code (MIT), well maintained. Defines the 'weak information' setting (features, structure and labels all incomplete). |
| [AGCL](../papers/wang2023-agcl/) | 2023 | C | 5 | IEEE TMM 2023 | [wangemm/AGCL-TMM-2022](https://github.com/wangemm/AGCL-TMM-2022) | BDGP, Caltech101, COIL20, MNIST-type sets | Priority 5 with official code (Apache-2.0). |
| [COMPLETER](../papers/lin2021-completer/) | 2021 | C | 4 | CVPR 2021 | [XLearning-SCU/2021-CVPR-Completer](https://github.com/XLearning-SCU/2021-CVPR-Completer) | Caltech101-20, LandUse-21, Scene-15, NoisyMNIST | Best-supported code in the multi-view group (134 stars, MIT, data included). The entry point for category C. |
| [DCG](../papers/zhang2025-dcg/) | 2025 | C | 4 | AAAI 2025 | [zhangyuanyang21/2025-AAAI-DCG](https://github.com/zhangyuanyang21/2025-AAAI-DCG) | CUB, HandWritten, Fashion and similar | Official code (32 stars), recent. Small diffusion on feature vectors, cheap. |
| [OT](../papers/muzellec2020-ot/) | 2020 | D | 4 | ICML 2020 | [BorisMuzellec/MissingDataOT](https://github.com/BorisMuzellec/MissingDataOT) | 23 UCI tabular sets | Official code (108 stars), tiny data. Needed anyway as the OT baseline behind GRIOT. |
| [GINN](../papers/spinelli2020-ginn/) | 2020 | D | 4 | Neural Networks 2020 | [spindro/GINN](https://github.com/spindro/GINN) | 20 UCI tabular sets | Official code (78 stars, Apache-2.0). Old dependencies (2020 PyTorch/DGL), so expect porting work on torch 2.7. |
| [GRAPE](../papers/you2020-grape/) | 2020 | D | 4 | NeurIPS 2020 | [maxiaoba/GRAPE](https://github.com/maxiaoba/GRAPE) | 9 UCI tabular sets | Official code (151 stars, MIT). The repo is ~2 GB with history; use a shallow clone. Key baseline for 'tabular data as a bipartite graph'. |
| [zhang2024-dirichlet](../papers/zhang2024-dirichlet/) | 2024 | D | 4 | KDD 2024 (to confirm) | [liguanlue/GLPN](https://github.com/liguanlue/GLPN) | UCI tabular sets; traffic METR-LA, PEMS | Official code (GLPN). Data small. Good bridge between tabular and graph-signal imputation. |

## Tier 2 - feasible with caveats

| Paper | Year | Cat. | Prio | Venue | Official code | Data | Notes |
|---|---|---|---|---|---|---|---|
| [PaGNN](../papers/jiang2021-pagnn/) | 2021 | A | 4 | arXiv 2021 | [yaya1015/PaGCN](https://github.com/yaya1015/PaGCN) | Cora, Citeseer, AmaPhoto, AmaComp | Simple partial-aggregation layer, a standard baseline. Use the authors' PaGCN repo (journal version, see zhang2024-pagc); the FP repo also contains a reimplementation. Do this and zhang2024-pagc as one unit. |
| [PaGC](../papers/zhang2024-pagc/) | 2024 | A | 4 | IEEE TAI 2024 | [yaya1015/PaGCN](https://github.com/yaya1015/PaGCN) | Cora, Citeseer, AmaPhoto, AmaComp, Cora-ML, Flickr | Journal version of PaGNN with official code (MIT). Reproduce together with jiang2021-pagnn. |
| [APP](../papers/li2026-app/) | 2026 | A | 4 | IEEE TNNLS 2026 | [limengran98/APP](https://github.com/limengran98/APP) | Heterophilic sets: Roman-empire, Amazon-ratings, Minesweeper, Tolokers, Questions, Squirrel, Chameleon | Official repo exists (no licence, no description; check that it is complete). Only paper here focused on heterophily, which makes it a useful contrast. |
| [moshiri2026-iaas](../papers/moshiri2026-iaas/) | 2026 | A | 4 | IEEE ICWS 2026 | [erfanmoshiri/graph-imputation](https://github.com/erfanmoshiri/graph-imputation) | Cora, CiteSeer, AMAC, AMAP; plus a private ~6M-node property graph (**partially open**) | Official code (MIT). Only the public-benchmark tables can be reproduced; the large real-estate graph is not released. |
| [MEGAE](../papers/gao2023-megae/) | 2023 | A | 3 | AAAI 2023 | [zqgao22/max-entropy-gae](https://github.com/zqgao22/max-entropy-gae) | Cora, Citeseer, PubMed, AmaPhoto, plus multi-graph sets | Official code, small (MIT). Spectral, eigendecomposition-based; fine on small graphs. Priority 3. |
| [Cold Brew](../papers/zheng2022-coldbrew/) | 2022 | B | 4 | ICLR 2022 | [amazon-science/gnn-tail-generalization](https://github.com/amazon-science/gnn-tail-generalization) | Cora, Citeseer, PubMed, ogbn-arxiv, Chameleon; plus 4 proprietary e-commerce sets (**partially open**) | Official code (Apache-2.0). Only the public-dataset tables are reproducible. About missing neighbourhoods (cold start), not missing attributes. |
| [RITR](../papers/tu2024-ritr/) | 2024 | B | 4 | IEEE TNNLS 2024 | none found | Cora, Citeseer, Amazon-Computers, Amazon-Photo | The WxTu/RITR repo is a placeholder (8 KB, no code), but RITR extends ITR, whose code is released. Reimplement on top of ITR. |
| [ProImp](../papers/li2023-proimp/) | 2023 | C | 4 | IJCAI 2023 | [XLearning-SCU/2023-IJCAI-ProImp](https://github.com/XLearning-SCU/2023-IJCAI-ProImp) | Scene-15, NoisyMNIST, Reuters, Caltech101 and similar | Official code (MIT), same group and data as COMPLETER. |
| [DMVG](../papers/wen2024-dmvg/) | 2024 | C | 4 | ICML 2024 | [Dshijie/DMVG](https://github.com/Dshijie/DMVG) | Caltech7 and other clustering sets; image sets Multi-Modal CelebA-HQ, Carl, NH-face | Official code (~475 MB repo). Image diffusion experiments need tens of GB and long training; reproduce the clustering tables only. |
| [CPSPAN](../papers/jin2023-cpspan/) | 2023 | C | 3 | CVPR 2023 | [jinjiaqi1998/CPSPAN](https://github.com/jinjiaqi1998/CPSPAN) | Caltech101, HandWritten and other multi-view feature sets | Official code, small feature files. Priority 3; multi-view, outside the graph core. |
| [CSCR](../papers/wang2025-cscr/) | 2025 | C | 3 | IEEE TMM 2025 | [wangemm/CSCR-TMM-2025](https://github.com/wangemm/CSCR-TMM-2025) | Corel5k, Pascal07, ESPGame, IAPRTC12, Mirflickr | Official code. Priority 3; multi-label classification, furthest from the graph core. |
| [GANImputer](../papers/wang2025-ganimputer/) | 2025 | D | 3 | Neural Computing and Applications 2025 | [hongyuchen2andrew/GANImputer](https://github.com/hongyuchen2andrew/GANImputer) | 4 UCI sets, 1 Kaggle set, Tennessee Eastman process | Official code exists (no licence, zero stars). Priority 3; tabular, not graph. |
| [FairAC](../papers/guo2023-fairac/) | 2023 | E | 4 | ICLR 2023 | [donglgcn/FairAC](https://github.com/donglgcn/FairAC) | NBA, Pokec-z, Pokec-n | Official code (MIT) with data. Niche (fair attribute completion); do after the core imputation methods. |
| [FairGNN](../papers/dai2022-fairgnn/) | 2022 | E | 0 | IEEE TKDE 2022 | [EnyanDai/FairGNN](https://github.com/EnyanDai/FairGNN) | Pokec-z, Pokec-n, NBA (in repo) | Code and data are available, but the paper is about fairness, not imputation (priority 0). Only worth running as the baseline FairAC needs. |

## Tier 3 - from the paper only

| Paper | Year | Cat. | Prio | Venue | Official code | Data | Notes |
|---|---|---|---|---|---|---|---|
| [DTRGC](../papers/hu2025-dtrgc/) | 2025 | A | 5 | ACM MM 2025 | none found | Cora, Citeseer, PubMed, Amazon-Photo, Amazon-Computers | Priority 5 but no official code found. Data is standard, so a from-paper implementation is feasible; expect a gap against reported clustering numbers. |
| [GDN](../papers/li2021-deconv/) | 2021 | A | 4 | NeurIPS 2021 | none found | Cora, Citeseer, AmaPhoto, AmaComp, Douban, Ciao (10% uniform missing) | No official code found. Only the feature-imputation half of the paper is relevant here. |
| [SAGA](../papers/tu2021-saga/) | 2021 | A | 4 | arXiv 2021 | none found | Cora, Citeseer, Amazon sets, Coauthor-CS | No official code found. Superseded by the same group's ITR/RITR/WAGE; low value on its own. |
| [AMGCL](../papers/zhang2023-amgcl/) | 2023 | A | 4 | arXiv 2023 | none found | Cora, CiteSeer, PubMed, Photo, Computers, Steam | A repo limengran98/AmGCL exists but is empty (1 KB), so treat as no code. |
| [CSAT](../papers/li2024-csat/) | 2024 | A | 4 | IEEE TCSS 2024 | none found | Cora, CiteSeer, PubMed, Amazon, Reddit/Flickr-scale sets (nine public sets) | No official code found. Transformer with sampling; community detection on attribute-missing graphs. |
| [AIAE](../papers/xia2024-aiae/) | 2024 | A | 4 | Knowledge-Based Systems 2024 | none found | Cora, Citeseer, Amazon-Computers, Amazon-Photo | No official code found. |
| [WGNN](../papers/chen2025-wgnn/) | 2025 | A | 4 | IEEE TPAMI 2025 | none found | Cora, Citeseer-type citation graphs, Wisconsin, Chameleon, synthetic | No official code found. Needs Wasserstein barycenters (POT). Method is involved (three variants); reimplementing from the paper is a real effort. |
| [ATS](../papers/liu2025-ats/) | 2025 | A | 4 | arXiv 2025 | none found | Cora, Citeseer, Amazon-Photo, Steam | No official code found. It is a sampling add-on to SAT, so it becomes cheap once chen2022-sat runs. |
| [EGS](../papers/song2025-egs/) | 2025 | A | 4 | Scientific Reports 2025 | none found | Cora, Citeseer, Photo, Computers | No official code found (open-access paper). |
| [MV-MDCC](../papers/song2025-mvmdcc/) | 2025 | A | 4 | Complex & Intelligent Systems 2026 | none found | Cora, Citeseer, Photo, Computers | No official code found. Same authors and setting as song2025-egs. |
| [Graphiam](../papers/xia2025-graphiam/) | 2025 | A | 4 | conference paper 2025 | none found | Cora, Citeseer, Amazon-Computers, Amazon-Photo (imbalanced splits via GraphMixup) | No official code found. Needs the class-imbalance protocol from GraphMixup on top of imputation. |
| [MOBA](../papers/yu2025-moba/) | 2025 | A | 4 | Int. J. Machine Learning and Cybernetics 2025 | none found | Cora, Citeseer, Amazon-Computers, Amazon-Photo | No official code found. |
| [AMMGC](../papers/zhao2025-ammgc/) | 2025 | A | 4 | CVPR 2025 | none found | Cora, Citeseer and two more graph benchmarks | No official code found (an unrelated 2021 repo shares the name). |
| [WAGE](../papers/tu2026-wage/) | 2026 | A | 3 | IEEE TPAMI 2025 | none found | Cora, Citeseer, Amazon-Computers, Amazon-Photo | No official code found. Priority 3. Builds on ITR, so the ITR code is a starting point. |
| [lei2026-weaksup](../papers/lei2026-weaksup/) | 2026 | B | 5 | IEEE/CAA J. Automatica Sinica 2026 | none found | Cora, Citeseer, PubMed and similar | Priority 5 but no official code found. Extends D2PT's setting, so reproduce liu2024-d2pt first and build on it. |
| [UGCL](../papers/fu2023-ugcl/) | 2023 | B | 4 | IEEE ICDM 2023 | none found | Cora, Citeseer, Chameleon, Squirrel, Cornell, Texas, Wisconsin | No official code found. Short paper (6 pages), so details may be missing. |
| [MDS-GNN](../papers/yuan2024-mdsgnn/) | 2024 | B | 4 | IEEE SMC 2024 | none found | Cora, CiteSeer, Photo, Chameleon | No official code found. Short paper (6 pages). |
| [DRI](../papers/liu2025-dri/) | 2025 | B | 4 | Knowledge-Based Systems 2025 | none found | Cora, Citeseer, Chameleon, Squirrel, Cornell, Texas, Wisconsin (T2-GNN data) | No official code found. Uses T2-GNN's released data, so the data side is exact. |
| [RGCN](../papers/qiu2026-rgcn/) | 2026 | B | 4 | arXiv 2026 | none found | ACM, DBLP, REUT, HHAR and similar clustering sets | Preprint, no code found. Lower value until published. |
| [ACTIVE](../papers/wang2022-active/) | 2022 | C | 5 | IJCAI 2022 | none found | BDGP, MNIST-USPS, Caltech101-type sets | Priority 5, but no official code found. The same authors released code for the follow-up AGCL (wang2023-agcl); reproduce that first and derive ACTIVE from it. |
| [AIMC](../papers/xu2021-aimc/) | 2021 | C | 4 | IEEE TCYB 2022 | none found | Handwritten, BDGP, Animal, CUB, Reuters | No official code found. Adversarial training, older stack. |
| [DIMvSML](../papers/li2024-dimvsml/) | 2024 | C | 4 | ACM MM 2024 (to confirm) | none found | Yeast, Corel5k, Pascal07, ESPGame, IAPRTC12, Mirflickr | No official code found. Data are the standard multi-view multi-label feature sets (shipped with DICNet/LMVCAT). |
| [AGDIMC](../papers/pu2024-agdimc/) | 2024 | C | 4 | AAAI 2024 | none found | BDGP, Reuters and one more public multi-view set | No official code found. |
| [DGGI-Net](../papers/mao2026-dgginet/) | 2026 | C | 4 | J. King Saud Univ. CIS 2026 | none found | Corel5k, Pascal07, ESPGame, IAPRTC12, Mirflickr | No official code found; unedited early-access version. |
| [DISCM](../papers/pan2026-discm/) | 2026 | C | 4 | Multimedia Systems 2026 | none found | LandUse-21, HandWritten, CUB, NoisyMNIST, synthetic | No official code found; data statement says no datasets generated. Diffusion model, more training time than the rest of C. |

## Tier 4 - defer

| Paper | Year | Cat. | Prio | Venue | Official code | Data | Notes |
|---|---|---|---|---|---|---|---|
| [R-AMGC](../papers/wang2026-ramgc/) | 2026 | A | 4 | under review at ICLR 2026 (anonymous) | none found | four citation / co-purchase benchmarks | Anonymous submission, no code, final version and acceptance unknown. Wait for a published version. |
| [wu2023-gan-imputation](../papers/wu2023-gan-imputation/) | 2023 | D | 4 | IEEE ICDE 2023 | none found | Six public incomplete tables, some million-row (COVID-19 trials, weather, surveillance ...) | No official code found and the contribution is scalability of GAN imputers on very large tables. Poor fit for this project and for calypso's disk. |

## Compute and disk

Everything not listed here fits comfortably on calypso's root disk and one A40.

| Paper | Issue | Suggestion |
|---|---|---|
| GRAPE | Repository is ~2 GB with history | `git clone --depth 1`, or put it on `/mnt/raw` |
| DMVG | ~475 MB repo; image diffusion on CelebA-HQ, Carl, NH-face | Reproduce clustering tables only |
| FP, PCFI, FISF, D2PT, DART, FSD-CAP, AttriReBoost | ogbn-arxiv is fine (~200 MB); OGBN-Products (~1.4 GB download, several GB processed) and Reddit are optional | Do the small graphs first; put OGB data on `/mnt/raw` |
| GRIOT | OT cost grows quadratically with nodes; repo ~130 MB | Start with Cora/CiteSeer |
| Wu 2023 (SCIS) | Million-row tables, no code | Tier 4 |
| WGNN, GRIOT, OT | Need the `POT` package | Still awaiting Haris's OK to install (see `docs/compute.md`) |
| Nearly all graph papers | Need `torch_geometric` | Same |

## By category

| Category | Papers | With code | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---|---|---|---|---|---|---|
| A. Graphs with missing node attributes | 33 | 18 | 13 | 5 | 14 | 1 |
| B. Graphs with incomplete features and structure | 9 | 3 | 2 | 2 | 5 | 0 |
| C. Incomplete multi-view learning | 13 | 7 | 3 | 4 | 6 | 0 |
| D. General (tabular) data imputation | 6 | 5 | 4 | 1 | 0 | 1 |
| E. Fairness with missing attributes | 2 | 2 | 0 | 2 | 0 | 0 |
