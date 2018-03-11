# lowResourceNMT
Improve a baseline NMT system trained on a very small parallel corpus using either monolingual data or parallel data in other languages

### Datasets:
https://yadi.sk/d/xUKsoX-G3T6ZYc

### Workflow board:
https://trello.com/b/f3kcPkqm/low-resource-nmt

### Read articles:
1) Transfer Learning for Low-Resource Neural Machine Translation
2) Zero-shot translation

### How to run train-and-evaluation with he-en:
1) place your data in data/t2t_data/* (en.train.txt, he.train.txt - train, dev, test generate from these files)
2) run t2t_translation.sh
