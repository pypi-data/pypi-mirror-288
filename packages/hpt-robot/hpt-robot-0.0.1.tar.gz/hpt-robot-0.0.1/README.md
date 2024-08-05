# Transfer Learning for HPTs
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Static Badge](https://img.shields.io/badge/Project-Page-a)](liruiw.github.io/hpt)

[Arxiv]() [Website](https://liruiw.github.io/hpt)

This repository serves as the transfer learning for [HPT](https://github.com/liruiw/HPT-Pretrain) pretrained models.
![](doc/concept.png)


## ⚙️ Installation
1. ```pip install -e .```
2. This repository should share the `data` folder and the `output` folder as the [pretraining repo](https://github.com/liruiw/HPT-pretrain).

## 🚶 Usage
0. Check out ``quickstart.ipynb`` for how to use the pretrained HPTs.
1. ```python -m hpt.run``` train policies on each environment. Add `+mode=debug`  for debugging.
2. ```bash experiments/scripts/metaworld/train_test_metaworld_1task_notrunk_end2end.sh test test 1 +mode=debug``` for example script.

## 🤖 Try this On Your Own Dataset
0. For training, it requires a dataset conversion  `convert_dataset` function for packing your own datasets. Check [this](env/realworld) for example.
1. For evaluation, it requires a `rollout_runner.py` file for each benchmark. It requires  a ``learner_trajectory_generator`` evaluation function that provides rollouts (potentially with some associated fixed scenes).
2. If needed, modify the [config](experiments/configs/config.yaml) for changing the perception stem networks and action head networks in the models. Take a look at [`realrobot_image.yaml`](experiments/configs/env/realrobot_image.yaml) for example script.

---
## 💾 File Structure
```angular2html
├── ...
├── HPT-pretrain
├── HPT-transfer
|   ├── data            # cached datasets
|   ├── output          # trained models and figures
|   ├── env             # environment wrappers
|   ├── hpt             # model training and dataset source code
|   |   ├── models      # network models
|   |   ├── datasets    # dataset related
|   |   ├── run         # transfer learning main loop
|   |   ├── run_eval    # evaluation main loop
|   |   └── ...
|   ├── experiments     # training configs
|   |   ├── configs     # modular configs
└── ...
```

### Citation
If you find HPT useful in your research, please consider citing:
```
@inproceedings{wang2024hpt,
author    = {Lirui Wang, Xinlei Chen, Jialiang Zhao, Kaiming He},
title     = {Scaling Proprioceptive-Visual Learning with Heterogeneous Pre-trained Transformers},
booktitle = {Arxiv},
year      = {2024}
}
```