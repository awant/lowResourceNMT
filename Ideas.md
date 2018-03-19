1) BackTranslation




2) ForwardTranslation. Sennrich et al. (2015)




3) Semi-supervised (from other NMT tasks, e.g. make use of monolingual embeddings)
Problem: Word2Vec works not quite well on subwords
- stemming
- coverage 



4) Transfer learning from other NMT Task

-) Trained model (checkpoint) for ende translation: https://yadi.sk/d/6ahyjxGJ3TXQV3

-) Enabling Zero-Shot Translation
Introduces an artificial token at the beginning of the input sentence to specify the required target language.

Before: Hello, how are you? -> Hola, ¿cómo estás?
After: <2es> Hello, how are you? -> Hola, ¿cómo estás?

After over- or undersampling some of the data to adjust for the relative ratio of the language data available.

-) Transfer Learning for Low-Resource Neural Machine Translation

Parent model -> child model (+5.6 bleu in avg)

Initialized weights for child model with weights from parent model.
Fix some params and fine-tuning anothers.
For example:
Parent model: French–English, child model: Uzbek–English.
English word embeddings from parent model are copied.
Uzbek words are initially mapped to random French embeddings.
English embeddings are frozen.
