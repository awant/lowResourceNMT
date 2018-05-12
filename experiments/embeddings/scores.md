# Results

## 1. 20k dictionary, fully unsupervised (100k batches)

### Bleu scores (word level)

direction | stemmed | merged
----------|---------|--------
ru->en | 5.89 | 5.16
en->ru | 4.76 | 2.66
en->en | 76.25 | 74.70
ru->ru | 73.82 | 70.03


## 2. 20k dictionary, 100k parallel sentences (54k batches)

### Bleu scores (word level)

direction | stemmed | merged
----------|---------|--------
ru->en | 6.95 | 6.12
en->ru | 7.03 | 4.08
en->en | 74.04 | 72.10
ru->ru | 72.62 | 68.62


## 3. Random swap, 20k dict, unsupervised

### Bleu scores (word level)

direction | stemmed | merged
----------|---------|--------
ru->en | 6.34 | 5.65
en->ru | 4.74 | 2.69
