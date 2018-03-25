## Results

0. [Info](#0-info)
1. [Baseline](#1-baseline)
2. [Back-Forward Translation](#2-back-forward-translation)
3. [Transfer learning](#3-transfer-learning)


### 0. Info

1. bleu is nltk-bleu

2. one batch per step is viewed

3. batch_size is 4096

### 1. Baseline

#### hebrew-english

##### single-random-reference mode

results on new test ~ 29K

10K steps, 4096 batch_size:

train_size | bleu
---------- | ----
236K(0.8) | 0.63
88K(0.3) | 0.59
50K(0.17) | 0.51
29K(0.1) | 0.44
3K(0.01) | 0.05


50K train_size(~ 12 steps/epoch):

steps, K | bleu
---------|-----
10 | 51
11 | 51.9
13 | 52.3
18 | 52.4


236K train size(~ 58 steps/epoch)

steps, K | bleu
---------|-----
2 | 33
4 | 53
7 | 60
10 | 63.5
15 | 66
17 | 66.7
19 | 67
21 | 67.3
22 | 67.6
23 | 67.8

##### all-reference mode

236K train size:

results on new dev ~ 29K:

steps | bleu
------|-----
11K | 60.04
12K | 60.77
13K | 61.05
14K | 61.53
15K | 61.99
16K | 62.34
17K | 62.29
18K | 62.85
19K | 62.6
20K | 62.92

results on old dev ~ 4K:

he-en

steps | bleu
------|-----
11K | 56.29
12K | 57.45
13K | 57.76
14K | 57.74
15K | 58.69
16K | 58.93
17K | 58.91
18K | 59.52
19K | 58.97
20K | 59.14


en-he

steps | bleu
------|-----
4K | 61.07
5K | 66.86
6K | 68.86
7K | 70.81
8K | 71.06
9K | 73.22
10K | 73.71
11K | 74.29
12K | 74.99
13K | 75.27
14K | 75.77

results on old test ~ 1K:

steps | bleu
------|-----
11К | 53.10
12К | 48.07
13K | 51.84
14K | 45.06
15K | 43.86
16K | 48.39
17K | 48.29
18K | 48.79
19K | 52.30
20K | 46.69

### 2. Back-Forward Translation


results on new test ~ 29K:

setup | bleu
------|-----
100% train | 67
10% train | 42
10% train + 90% forward translated | 38
10% train + 90% back translated | 33

![curves](https://trello-attachments.s3.amazonaws.com/5a8c674b302a8b5b2f0d9cd8/5aa70addb0e4401313478392/d3badcb53695275879fbcc0000aada3e/forward.back.translate.png)


### 3. Transfer learning

Bla-bla-bla
