1) BackTranslation




2) ForwardTranslation. Sennrich et al. (2015)




3) Semi-supervised (from other NMT tasks, e.g. make use of monolingual embeddings)

Good starting point: https://arxiv.org/pdf/1710.11041v2.pdf

3.1. Trained monolinugal Russian/English embeddings on Wikipedia dumps. 

Tokenization: into stem/suffix (Snowball stemmer from nltk) 

Embeddings: Word2Vec (CBOW, window size = 5)


3.2. Shared embeddings space

In process


3.3. Encoder/Decoder model on shared embeddings

Shared encoder maps to hidden state

Two decoders for languages

Training: alternate between Denoising, On-the-fly backtranslation and Low-resource translation


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

5) 

-) Dual Learning for Machine Translation

Reinforcement learning with language models

Two-agent communication game:
A -> B, B -> A.
2 language models, 2 translation models. s -> s_{middle} -> s'

-) Unsupervised Neural Machine Translation Using Monolingual Corpora Only (similar idea/working on understanding)

6) Zero-shot translation
https://arxiv.org/pdf/1611.04558.pdf

7) Combination of different models
