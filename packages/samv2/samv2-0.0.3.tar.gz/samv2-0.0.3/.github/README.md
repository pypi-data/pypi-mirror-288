[![Build and Tests](https://github.com/SauravMaheshkar/samv2/actions/workflows/ci.yml/badge.svg)](https://github.com/SauravMaheshkar/samv2/actions/workflows/ci.yml)

## Installation

This is a CPU compatible fork of the official SAMv2 implementation. You can download it from [pypi](https://pypi.org/) using `pip` as follows:

```bash
pip install samv2
```

## Usage

After downloading the official weights, you can use the `load_model()` helper method to instantiate a model.

```python
from sam2 import load_model

model = load_model(
    variant="tiny",
    ckpt_path="artifacts/sam2_hiera_tiny.pt",
    device="cpu"
)
```

## Features 🚀

* CPU compatible
* ships with config files
* Run image and video inference on CPUs

## Citation

```bibtex
@article{ravi2024sam2,
  title={SAM 2: Segment Anything in Images and Videos},
  author={Ravi, Nikhila and Gabeur, Valentin and Hu, Yuan-Ting and Hu, Ronghang and Ryali, Chaitanya and Ma, Tengyu and Khedr, Haitham and R{\"a}dle, Roman and Rolland, Chloe and Gustafson, Laura and Mintun, Eric and Pan, Junting and Alwala, Kalyan Vasudev and Carion, Nicolas and Wu, Chao-Yuan and Girshick, Ross and Doll{\'a}r, Piotr and Feichtenhofer, Christoph},
  journal={arXiv preprint},
  year={2024}
}
```
