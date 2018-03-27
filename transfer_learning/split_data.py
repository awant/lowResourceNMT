#!/usr/bin/env python3
import numpy as np
import math
import argparse
import os

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

def make_split(input_folder, output_folder, train_size, dev_size, test_size):
    np.random.seed(42)
    ru_sents = load_sents(os.path.join(input_folder, 'ru.train.txt'))
    en_sents = load_sents(os.path.join(input_folder, 'en.train.txt'))
    assert(len(ru_sents) == len(en_sents))
    sents_count = len(ru_sents)
    print('sents_count = {}'.format(sents_count))

    train_size, dev_size, test_size = map(lambda x: math.floor(x * sents_count),
        (train_size, dev_size, test_size))

    new_idxs = np.random.choice(
        np.arange(sents_count), size=train_size + dev_size + test_size, replace=False
    )
    print('saving ru sentences...')

    with open(os.path.join(output_folder, 'ru.train.txt'), 'w') as fh:
        for i in range(train_size):
            fh.write(ru_sents[i])
    with open(os.path.join(output_folder, 'ru.dev.txt'), 'w') as fh:
        for i in range(train_size, train_size+dev_size):
            fh.write(ru_sents[i])
    with open(os.path.join(output_folder, 'ru.test.txt'), 'w') as fh:
        for i in range(train_size+dev_size, train_size+dev_size+test_size):
            fh.write(ru_sents[i])

    print('ru sentences saved')

    print('saving en sentences...')
    with open(os.path.join(output_folder, 'en.train.txt'), 'w') as fh:
        for i in range(train_size):
            fh.write(en_sents[i])
    with open(os.path.join(output_folder, 'en.dev.txt'), 'w') as fh:
        for i in range(train_size, train_size+dev_size):
            fh.write(en_sents[i])
    with open(os.path.join(output_folder, 'en.test.txt'), 'w') as fh:
        for i in range(train_size+dev_size, train_size+dev_size+test_size):
            fh.write(en_sents[i])
    print('en sentences saved')
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_folder', action='store', type=str, default='/data/lowResourceNMT/data/en-ru')
    parser.add_argument('--output_folder', action='store', type=str, default='/data/rimarakulin/en-ru-small_data/t2t_data')
    parser.add_argument('--train_size', action='store', type=float, help='train sample size', default=0.2)
    parser.add_argument('--dev_size', action='store', type=float, help='dev sample size', default=0.2)
    parser.add_argument('--test_size', action='store', type=float, help='test sample size', default=0.2)
    args = parser.parse_args()

    make_split(args.input_folder, args.output_folder, args.train_size, args.dev_size, args.test_size)

