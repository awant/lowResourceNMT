#!/usr/bin/env python3

import argparse
import numpy as np
from nltk.translate.bleu_score import corpus_bleu

def get_translations(path):
    with open(path, 'r') as fh:
        data = [x.rstrip() for x in fh.readlines()]
    return data

def get_references(path):
    with open(path, 'r') as fh:
        data = [x.rstrip().split('\t') for x in fh.readlines()]
    return data

def compute_bleu(references, candidates):
    if (type(references) is str) and (type(candidates) is str):
        references = get_references(references)
        candidates = get_translations(candidates)
        return compute_bleu(references, candidates)
    assert(len(references) == len(candidates))

    score = corpus_bleu(references, candidates)
    return score


# example: ./compute_bleu.py --translation=../data/t2t_data-10k/en.translation --reference=../data/t2t_data-10k/en.test.txt
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--translation', type=str, help='path to translation')
    parser.add_argument('--reference', type=str,
                        help='Path to file with references. Several references separated by tab')
    args = parser.parse_args()
    bleu = compute_bleu(args.reference, args.translation)
    print(bleu)
