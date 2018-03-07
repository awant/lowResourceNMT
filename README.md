# lowResourceNMT
Improve a baseline NMT system trained on a very small parallel corpus using either monolingual data or parallel data in other languages

### Datasets:
https://yadi.sk/d/xUKsoX-G3T6ZYc

### Read articles:
1) Transfer Learning for Low-Resource Neural Machine Translation
2) Zero-shot translation

### How to run train-and-evaluation with he-en:
1) place your data in data/t2t_data/* (en.train.txt, en.test.txt, en.dev.txt, he.train.txt, ...)
2) change ROOT_DATA_DIR (scripts/t2t_translation.py) to path in your PC
3) run scripts/t2t_translation.py (by default 10k steps, but you can run datagen-train-evaluation separately)
