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
en->en | 83.11 | 82.20
ru->ru | 81.41 | 80.61


## 4. Random swap, 20k dict, 100k parallel sentences

### Bleu scores (word level)

direction | stemmed | merged
----------|---------|--------
ru->en | 11.90 | 10.77
en->ru | 8.88 | 5.69
en->en | 82.17 | 81.44
ru->ru | 77.92 | 77.08

## 5. New 50k dict, training only on stems, 100k parallel sentences

### Bleu scores (word level)

direction | stemmed 
----------|---------
ru->en | 9.89 
en->ru | 8.93
en->en | 74.99
ru->ru | 71.24
