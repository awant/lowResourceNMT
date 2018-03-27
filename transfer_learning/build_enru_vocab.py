import sys
import argparse
from collections import defaultdict
from tensor2tensor.data_generators import text_encoder
from tensor2tensor.data_generators import tokenizer
from random import shuffle

PIPE_SYMBOL = ' ||| '


def get_vocab_mapping(filepath):
    mapping = {}
    with open(filepath) as f:
        for idx, line in enumerate(f):
            mapping[line.rstrip()] = idx
    return mapping

def itokenize(filepath):
    with open(filepath) as f:
        for line in f:
            line = line.rstrip()
            tokens = [tok for tok in tokenizer.encode(text_encoder.native_to_unicode(line))]
            yield tokens

def generate_subword_vocab(filepath):
    token_counts = defaultdict(int)
    for tokens in itokenize(filepath):
        for token in tokens:
            token_counts[token] += 1
    vocab = text_encoder.SubwordTextEncoder.build_to_target_size(1000, token_counts, 1, 1e3)
    # vocab = text_encoder.SubwordTextEncoder.build_from_token_counts(token_counts, 1000, 4, None, text_encoder.RESERVED_TOKENS)
    vocab.dump()
    return vocab


# generate_subword_vocab('de-ru/News-Commentary.de-ru.ru')
# sys.exit(0)

def create_fast_align_input(src_iter, trg_iter, filepath):
    with open(filepath, 'w') as f:
        for src_tokens, trg_tokens in zip(src_iter, trg_iter):
            f.write(' '.join(src_tokens) + PIPE_SYMBOL + ' '.join(trg_tokens)+'\n')

def get_tokens_mapping(fast_align_input_filepath, fast_align_result_filepath):
    def parse_tokens_from_line(parall_data_line):
        parall_data_line = parall_data_line.rstrip()
        src_tokens, trg_tokens = parall_data_line.split(PIPE_SYMBOL)
        return src_tokens.split(' '), trg_tokens.split(' ')

    def parse_alignments_from_line(alignment_line):
        alignment_line = alignment_line.strip()
        alignments = [[int(y) for y in x.split('-')] for x in alignment_line.split(' ')]
        return alignments

    mapping = {}
    with open(fast_align_input_filepath) as parall_data_f, open(fast_align_result_filepath) as alignments_f:
        for parall_data_line, alignment_line in zip(parall_data_f, alignments_f):
            src_tokens, trg_tokens = parse_tokens_from_line(parall_data_line)
            alignments = parse_alignments_from_line(alignment_line)
            # print('src_tokens: {}'.format(src_tokens))
            # print('trg_tokens: {}'.format(trg_tokens))
            # print('alignments: {}'.format(alignments))

            for src_idx, trg_idx in alignments:
                # TODO: make better (want sleep now so bad)
                if src_tokens[src_idx] not in mapping:
                    mapping[src_tokens[src_idx]] = {trg_tokens[trg_idx] : 0}
                if trg_tokens[trg_idx] not in mapping[src_tokens[src_idx]]:
                    mapping[src_tokens[src_idx]][trg_tokens[trg_idx]] = 0
                mapping[src_tokens[src_idx]][trg_tokens[trg_idx]] += 1
    result_mapping = {}
    for src_token, d in mapping.items():
        result_mapping[src_token] = max(mapping[src_token].keys(), key=(lambda x: mapping[src_token][x]))
    return result_mapping

def build_random_mapping(ende_vocab_path, enru_vocab_path, result_vocab_path):
    ende_mapping = get_vocab_mapping(ende_vocab_path)
    enru_mapping = get_vocab_mapping(enru_vocab_path)
    print('subwords lengths: ende={}, enru={}'.format(len(ende_mapping), len(enru_mapping)))

    fixed_idxs = set([val for key, val in ende_mapping.items() if key in enru_mapping])
    import pickle
    with open('fixed_idxs.pickle', 'wb') as f:
        pickle.dump(fixed_idxs, f, pickle.HIGHEST_PROTOCOL)

    return

    enru_exclusive_tokens = [key for key in enru_mapping.keys() if key not in ende_mapping]
    ende_exclusive_tokens = [key for key in ende_mapping.keys() if key not in enru_mapping]
    print('should map {} enru exclusive tokens into {} ende exclusive tokens'.format(len(enru_exclusive_tokens),
        len(ende_exclusive_tokens)))
    # make ende_exclusive_tokens shuffling
    shuffle(ende_exclusive_tokens)

    for ru_token, de_token in zip(enru_exclusive_tokens, ende_exclusive_tokens):
        # print('{}->{}'.format(ru_token, de_token))
        ende_mapping[ru_token] = ende_mapping[de_token]
        ende_mapping.pop(de_token)
    idx_to_token = {idx: token for token, idx in ende_mapping.items()}
    with open(result_vocab_path, 'w') as f:
        for i in range(len(idx_to_token)):
            f.write(idx_to_token[i]+'\n')
    print('done')


def build_dict(ende_vocab_path, enru_vocab_path, result_vocab_path):
    ende_mapping = get_vocab_mapping(ende_vocab_path)
    enru_mapping = get_vocab_mapping(enru_vocab_path)
    print('ende_mapping', len(ende_mapping))
    print('enru_mapping', len(enru_mapping))
    print('matching', len({key: value for key, value in ende_mapping.items() if key in enru_mapping}))

    ende_lack = {key: value for key, value in ende_mapping.items() if key not in enru_mapping}
    print('ende_lack', len(ende_lack))
    for i, (val, idx) in enumerate(ende_lack.items()):
        if i > 50:
            break
        print(val, idx)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ende_vocab_path', action='store', type=str, default='vocab.ende.32768')
    parser.add_argument('--enru_vocab_path', action='store', type=str, default='vocab.enru.32768')
    parser.add_argument('--result_vocab_path', action='store', type=str, default='vocab.enru.32768.new')
    parser.add_argument('--mapping', action='store', type=str, default='random',
        help='Options of generated dictionary')
    args = parser.parse_args()

    if args.mapping == 'random':
        build_random_mapping(args.ende_vocab_path, args.enru_vocab_path, args.result_vocab_path)
    else:
        raise NotImplemented('check mapping option! Should be one of these: random')



    # i = 0
    # for tokens in itokenize('de-ru/News-Commentary.de-ru.ru'):
    #     i += 1
    #     if i > 320:
    #         break
    #     if i < 310:
    #         continue
    #     print(tokens)

    # print(next(itokenize('de-ru/News-Commentary.de-ru.ru')))
    # generate_subword_vocab('de-ru/News-Commentary.de-ru.ru')
    # sys.exit(1)
    # fast_align_input_filepath = '/Users/romanmarakulin/SDA/NLP/lowResourceNMT/en-ru-data/fast_align_input.txt'
    # fast_align_result_filepath = '/Users/romanmarakulin/SDA/NLP/lowResourceNMT/fast_align/build/forward.align'

    # ru_text_filepath = 'de-ru/News-Commentary.de-ru.ru'
    # de_text_filepath = 'de-ru/News-Commentary.de-ru.de'
    # create_fast_align_input(itokenize(ru_text_filepath), itokenize(de_text_filepath), 'ru_de_alig_input.txt')

    # tokens_mapping = get_tokens_mapping('ru_de_alig_input.txt', 'ru_de_forward.align')
    # for i, (src_token, trg_token) in enumerate(tokens_mapping.items()):
    #     if i > 50:
    #         break
    #     print('{} -> {}'.format(src_token, trg_token))
    # sys.exit(0)

    # build_dict(args.ende_vocab_path, args.enru_vocab_path, args.result_vocab_path)
