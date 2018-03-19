# lowResourceNMT
Improve a baseline NMT system trained on a very small parallel corpus using either monolingual data or parallel data in other languages

### Datasets:
https://yadi.sk/d/xUKsoX-G3T6ZYc

### Workflow board:
https://trello.com/b/f3kcPkqm/low-resource-nmt

### Tensor2Tensor
[Forked Tensor2Tensor version](https://github.com/AlAntonov/tensor2tensor)

Install from local dir: pip install -e tensor2tensor/

### Results:
Dataset | Model | Parameters | Score
------- | ----- | ---------- | -----

### Read articles:
[Attention Is All You Need](https://arxiv.org/abs/1706.03762)

[Unsupervised Neural Machine Translation Using Monolingual Corpora Only](https://arxiv.org/pdf/1711.00043)

[Zero-shot translation](https://arxiv.org/pdf/1611.04558)

[Dual learning for Machine Translation](https://arxiv.org/abs/1611.00179)

[Transfer Learning for Low-Resource Neural Machine Translation](https://www.aclweb.org/anthology/D16-1163)

[Adversarial Neural Machine Translation](https://arxiv.org/abs/1704.06933)

[Improving Neural Machine Translation with Conditional Sequence Generative Adversarial Nets](https://arxiv.org/pdf/1703.04887)

[On Using Monolingual Corpora in Neural Machine Translation](http://arxiv.org/abs/1503.03535)

[Improving Neural Machine Translation Models with Monolingual Data](http://arxiv.org/abs/1511.06709)

[Inducing Bilingual Lexica From Non-Parallel Data With Earth Mover’s Distance Regularization](http://aclweb.org/anthology/C16-1300.pdf)

[Exploiting Source-side Monolingual Data in Neural Machine Translation](https://pdfs.semanticscholar.org/cf58/f472413073009134e24c466b5a7385a14126.pdf)

[Unsupervised Pretraining for Sequence to Sequence Learning](http://aclweb.org/anthology/D17-1039)

[Universal Neural Machine Translation for Extremely Low Resource Languages](https://arxiv.org/pdf/1802.05368.pdf)

[Joint Training for Neural Machine Translation Models with Monolingual Data](https://arxiv.org/pdf/1803.00353.pdf)

[Unsupervised Neural Machine Translation](https://arxiv.org/pdf/1710.11041v2.pdf)

### How to run train-and-evaluation with he-en:
1) place your data in data/t2t_data/* (en.train.txt, he.train.txt - train, dev, test generate from these files)
2) run he-en_translation.sh (with options, train/dev/test sizes, etc - check script for more info)

### Features:
1) Sizes can be fractional. For example: he-en_translation.sh --train_size 0.4 --test_size 0.3 --dev_size 0.3
2) compute_bleu.py with flag --bootstrap return 95% confidence interval
