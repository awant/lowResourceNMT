#!/usr/bin/env python3

import numpy as np
import math
import argparse
import os

ru_filepath = 'ruen_data/corpus.en_ru.1m.ru'
en_filepath = 'ruen_data/corpus.en_ru.1m.en'
target_folder = 'ruen_split_data'

def load_sents(filepath):
    with open(filepath, 'r') as fh:
        return fh.readlines()

def save_to_file(data, lang, type):
    np.savetxt(X=data, fname=os.path.join(
        'ruen_split_data',
        "{}.{}.txt".format(lang, type)
        ),
        delimiter='\n', fmt='%s', encoding='utf-8'
    )

def save_to_file_dict(data):
    for (lang, type), sents in data.items():
        save_to_file(sents, lang, type)

def make_split(train_size, dev_size, test_size):
    np.random.seed(42)
    ru_sents = load_sents(ru_filepath)
    en_sents = load_sents(en_filepath)
    assert(len(ru_sents) == len(en_sents))
    sents_count = len(ru_sents)
    print('sents_count = {}'.format(sents_count))

    train_size, dev_size, test_size = map(lambda x: math.floor(x * sents_count),
        (train_size, dev_size, test_size))

    new_idxs = np.random.choice(
        np.arange(sents_count), size=train_size + dev_size + test_size, replace=False
    )
    print('before sents')

    with open(os.path.join(target_folder, 'ru.train.txt'), 'w') as fh:
        for i in range(train_size):
            fh.write(ru_sents[i])
    with open(os.path.join(target_folder, 'ru.dev.txt'), 'w') as fh:
        for i in range(train_size, train_size+dev_size):
            fh.write(ru_sents[i])
    with open(os.path.join(target_folder, 'ru.test.txt'), 'w') as fh:
        for i in range(train_size+dev_size, train_size+dev_size+test_size):
            fh.write(ru_sents[i])

    print('ru sentences saved')

    with open(os.path.join(target_folder, 'en.train.txt'), 'w') as fh:
        for i in range(train_size):
            fh.write(en_sents[i])
    with open(os.path.join(target_folder, 'en.dev.txt'), 'w') as fh:
        for i in range(train_size, train_size+dev_size):
            fh.write(en_sents[i])
    with open(os.path.join(target_folder, 'en.test.txt'), 'w') as fh:
        for i in range(train_size+dev_size, train_size+dev_size+test_size):
            fh.write(en_sents[i])

    print('en sentences saved')



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_size', action='store', type=float, help='train sample size', required=True)
    parser.add_argument('--dev_size', action='store', type=float, help='dev sample size', required=True)
    parser.add_argument('--test_size', action='store', type=float, help='test sample size', required=True)
    args = parser.parse_args()

    make_split(args.train_size, args.dev_size, args.test_size)