#!/usr/bin/env python3

import argparse
import numpy as np
from nltk.translate.bleu_score import corpus_bleu

def get_translations(path):
    with open(path, 'r') as fh:
        data = [x.rstrip() for x in fh.readlines()]
    return np.array(data)

def get_references(path):
    with open(path, 'r') as fh:
        data = [x.rstrip().split('\t') for x in fh.readlines()]
    return np.array(data)


def compute_bleu(references, candidates):
    if (type(references) is str) and (type(candidates) is str):
        references = get_references(references)
        candidates = get_translations(candidates)
        return compute_bleu(references, candidates)
    assert(len(references) == len(candidates))

    score = corpus_bleu(references, candidates)
    return score


def compute_bleu_bootstrap(references, candidates, confidence_interval=0.95, resamples_count=None):
    references = get_references(references)
    candidates = get_translations(candidates)
    assert(len(references) == len(candidates))

    n = len(references)
    # feel free to change this - can be very slow
    resamples_count = 400 if resamples_count is None else resamples_count

    def get_randomized_bleu():
        samples_idxs = np.random.choice(len(references), resamples_count)
        return compute_bleu(references[samples_idxs], candidates[samples_idxs])

    bleus = [get_randomized_bleu() for _ in range(resamples_count)]
    bleu_mean = np.mean(bleus)
    bleu_var = np.var(bleus)

    p = ((1. - confidence_interval)/2) * 100
    lower = np.percentile(bleus, p)
    p = (confidence_interval + (1. - confidence_interval)/2) * 100
    upper = np.percentile(bleus, p)

    return bleu_mean, np.sqrt(bleu_var), (lower, upper)


# example: ./compute_bleu.py --translation=../data/t2t_data-10k/en.translation --reference=../data/t2t_data-10k/en.test.txt
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--translation', type=str, help='path to translation')
    parser.add_argument('--reference', type=str,
                        help='Path to file with references. Several references separated by tab')
    parser.add_argument('--bootstrap', action="store_true", help='Is use bootstrap variant of bleu')
    args = parser.parse_args()

    if args.bootstrap:
        confidence_interval = 0.95
        bleu_mean, d, (lower, upper) = compute_bleu_bootstrap(args.reference, args.translation, confidence_interval)
        print('bleu mean: {:0.2f}, sqrt(var): {:0.2f}, CI-{:0.2f}: ({:0.2f}, {:0.2f})'.format(bleu_mean, d, confidence_interval, lower, upper))
    else:
        bleu = compute_bleu(args.reference, args.translation)
        print(bleu)
