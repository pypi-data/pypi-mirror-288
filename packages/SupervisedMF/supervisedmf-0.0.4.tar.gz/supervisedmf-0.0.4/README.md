# Supervised Matrix Factorization

This Python package contains source codes for algorithms for Supervised Matrix Factorization (SMF) in the papers [1] and [2]: 

## Installation

To install the package, run the following command in your environment:

```
python3 -m pip install SupervisedMF
```

Check your installation by trying to import the main classes in this package:

```
>>> from SMF import SMF_BCD
>>> from SMF import SMF_LPGD
```

## Pytorch Version

If you are looking to use the Pytorch version of the Supervised Matrix Factorization algorithms, please first install `torch` and its related dependencies in your environment using the appropriate command from [the official installation page](https://pytorch.org/get-started/locally/). 

For example, if you want to install `torch` for Linux with CUDA 12.1 using `pip`, run the following command:

```
pip3 install torch torchvision torchaudio
```

## References

[1] Lee, Joowon, Hanbaek Lyu, and Weixin Yao. [*"Exponentially convergent algorithms for supervised matrix factorization."*](https://papers.nips.cc/paper_files/paper/2023/hash/f2c80b3c9cf8102d38c4b21af25d9740-Abstract-Conference.html) Advances in Neural Information Processing Systems 36 (2024).

[2] Lee, Joowon, Hanbaek Lyu, and Weixin Yao. [*"Supervised Matrix Factorization: Local Landscape Analysis and Applications."*](https://proceedings.mlr.press/v235/lee24p.html) Forty-first International Conference on Machine Learning (2024).