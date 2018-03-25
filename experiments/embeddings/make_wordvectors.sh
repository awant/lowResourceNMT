#!/bin/bash

#### Set your hyper-parameters here ####
############## START ###################
lcode=$1 # ISO 639-1 code of target language. See `lcodes.txt`. example: ru, en
part=$2 # from 0 to 1 - part of corpus
max_corpus_size=1000000000 # the maximum size of the corpus. Feel free to adjust it according to your computing power.
vector_size=300 # the size of a word vector
window_size=5 # the maximum distance between the current and predicted word within a sentence.
vocab_size=20000 # the maximum vocabulary size
num_negative=5 # the int for negative specifies how many “noise words” should be drawn
workers=24 # u definetily need to change that number
############## END #####################

echo "step 0. Make 'data' directory."
mkdir data;

echo "step 1. Build Corpus."
python build_corpus.py --part=${part} --lcode=${lcode} --max_corpus_size=${max_corpus_size} --workers=24

echo "step 2. make wordvectors"
python make_wordvectors.py  --workers=${workers} --lcode=${lcode} \
                    --vector_size=${vector_size} --window_size=${window_size} \
                    --vocab_size=${vocab_size} --num_negative=${num_negative}
