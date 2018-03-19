1. bleu is nltk-bleu

2. one batch per step is viewed

## Baseline

### hebrew-english

#### single-random-reference mode

results on new he.test ~ 29K

10K steps, 4096 batch_size:

train_size | bleu
---------- | ----
236K(0.8) | 0.63
88K(0.3) | 0.59
50K(0.17) | 0.51
29K(0.1) | 0.44
3K(0.01) | 0.05


50K train_size, 4096 batch_size(~ 12 steps/epoch):

steps, K | bleu
---------|-----
10 | 51
11 | 51.9
13 | 52.3
18 | 52.4


236K train size, 4096 batch_size(~ 58 steps/epoch):

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

