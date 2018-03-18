#!/usr/bin/env python3

import argparse
import numpy as np
import os
from collections import defaultdict
import sys
import math

INT_MULTIPLIER = 1000

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def save_to_file(data, lang, dir, type):
    np.savetxt(X=data, fname=os.path.join(
        dir,
        "{}.{}.txt".format(lang, type)
        ),
        delimiter='\n', fmt='%s', encoding='utf-8'
    )

def make_mapping(first, second):
    data_first = np.loadtxt(first, dtype='str', encoding='utf-8')
    data_second = np.loadtxt(second, dtype='str', encoding='utf-8')

    mapping = defaultdict(set)

    for word, translation in zip(data_first, data_second):
        mapping[word].add(translation)

    return mapping

# unwind mapping
def get_words_and_references(words, mapping):
    pairs = []
    for word in words:
        pairs += [(word, ref_word) for ref_word in mapping[word]]
    return list(zip(*pairs))

def make_small_datasets(datapath, train_size, test_size, dev_size, all_transliterations=True):
    np.random.seed(42)
    train_dev_test_sizes_ar = [train_size, dev_size, test_size]

    is_float_sizes = not train_size.is_integer()
    if not is_float_sizes:
        train_dev_test_sizes_ar = list(map(lambda x: x * INT_MULTIPLIER, train_dev_test_sizes_ar))

    if datapath.endswith('/'):
        datapath = datapath[:-1]

    prefix = datapath.split('/')[-1]

    train_files, langs = [], []

    for filename in os.listdir(datapath):
        if filename.split('.')[1] == 'train':
            train_files.append(filename)
            langs.append(filename.split('.')[0])

    train_first, train_second = train_files
    lang_first, lang_second = langs

    if train_second.split('.')[0] == 'he':
        train_first, train_second = train_second, train_first
        lang_first, lang_second = lang_second, lang_first

    mapping = make_mapping(os.path.join(datapath, train_first), os.path.join(datapath, train_second))

    total_words = len(mapping)
    words = np.array(list(mapping.keys()))

    print('all words: {}'.format(total_words))
    if is_float_sizes:
        train_dev_test_sizes_ar = map(lambda x: math.floor(x * total_words), train_dev_test_sizes_ar)

    train_size, dev_size, test_size = [int(x) for x in train_dev_test_sizes_ar]
    print('splitting: train/dev/test = {}/{}/{}'.format(train_size, dev_size, test_size))

    assert(total_words >= train_size + test_size + dev_size)
    assert((train_size > 0) and (test_size > 0) and (dev_size > 0))

    new_ix = np.random.choice(
        a=np.arange(total_words), size=train_size + test_size + dev_size, replace=False
    )

    new_train_words = words[new_ix[:train_size]]
    new_test_words = words[new_ix[train_size: -dev_size]]
    new_dev_words = words[new_ix[-dev_size:]]

    if all_transliterations:
        new_train_words, new_train_translations = get_words_and_references(new_train_words, mapping)
        new_dev_words, new_dev_translations = get_words_and_references(new_dev_words, mapping)
    else:
        new_train_translations = [mapping[word].pop() for word in new_train_words]
        new_dev_translations = [mapping[word].pop() for word in new_dev_words]
    
    new_test_translations = ['\t'.join([translation for translation in mapping[word]]) for word in new_test_words]

    new_prefix = "{}-{}k".format(prefix, train_size // 1000)

    new_datadir = os.path.join('/'.join(datapath.split('/')[:-1]), new_prefix)

    if not os.path.exists(new_datadir):
        os.makedirs(new_datadir)

    print("Saving to {}".format(new_datadir))

    save_to_file(new_train_words, lang_first, new_datadir, 'train')
    save_to_file(new_test_words, lang_first, new_datadir, 'test')
    save_to_file(new_dev_words, lang_first, new_datadir, 'dev')

    save_to_file(new_train_translations, lang_second, new_datadir, 'train')
    save_to_file(new_test_translations, lang_second, new_datadir, 'test')
    save_to_file(new_dev_translations, lang_second, new_datadir, 'dev')


def check_args(args):
    for lang in ['he', 'en']:
        filepath = os.path.join(args.datadir, lang+'.train.txt')
        if not os.path.isfile(filepath):
            eprint('{} not exists!'.format(filepath))
            return False

    size_args = list(filter(lambda x: x in args, ['train_size', 'test_size', 'dev_size']))
    if len(size_args) < 2:
        eprint('only 1 of size arguments can be missed!')
        return False

    # check that all size_args integers or all size_args floats
    is_int_sizes = [getattr(args, size_arg).is_integer() for size_arg in size_args]
    if not (is_int_sizes.count(is_int_sizes[0]) == len(is_int_sizes)):
        eprint('all size arguments should be integers or all should be float!')
        return False

    # check that if float sizes, then sum of 3 <= 1.0, sum of 2 < 1.0
    if (is_int_sizes[0] is False) and (sum([getattr(args, size_arg) for size_arg in size_args]) > 1.0):
        eprint('sum of float sizes should be <= 1!')
        return False

    if len(list(filter(lambda x: x < 0, [getattr(args, size_arg) for size_arg in size_args]))) > 0:
        eprint('sizes should be > 0!')
        return False

    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--datadir', action='store', type=str, required=True,
                        help='Directory of original dataset. Should have .train.txt files in it.')
    parser.add_argument('--train_size', action='store', type=float, help='train sample size')
    parser.add_argument('--test_size', action='store', type=float, help='test sample size')
    parser.add_argument('--dev_size', action='store', type=float, help='dev sample size')
    parser.add_argument('--all_transliterations', action='store', type=bool, default=False,
                        help='Add all transliteration choices to train/dev sets')

    args = parser.parse_args()

    if check_args(args):
        make_small_datasets(args.datadir, args.train_size, args.test_size, args.dev_size, args.all_transliterations)
    else:
        sys.exit(-1)
