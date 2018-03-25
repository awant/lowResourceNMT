# coding: utf-8
#!/usr/bin/python2
import argparse
import codecs
import lxml.etree as ET
import os
import regex
import numpy as np

from tokenizer import SentenceTokenizer


DUMP_DATE = "20180301"

# arguments setting
parser = argparse.ArgumentParser()
parser.add_argument('--lcode', help='ISO 639-1 code of target language.')
parser.add_argument('--part', type=float, default=1, help='part of corpus')
parser.add_argument('--workers', type=int, default=3, help='the number of workers')
parser.add_argument('--max_corpus_size', type=int, default=1000000000, help='the maximum size of the corpus. Feel free to adjust it according to your computing power.')
args = parser.parse_args()
workers = args.workers
part = args.part

ST = SentenceTokenizer(lang=args.lcode)

lcode = args.lcode
if lcode == 'ko':
    from konlpy.tag import Kkma # pip install konlpy. See http://konlpy.org/en/v0.4.4/ for further information.
    kkma = Kkma()
elif lcode == 'ja':
    import MeCab # See https://pypi.python.org/pypi/mecab-python/0.996
    mecab = MeCab.Tagger("-Owakati")
elif lcode == 'zh':
    import jieba # See https://pypi.python.org/pypi/jieba/
elif lcode == 'vi':
    from pyvi.pyvi import ViTokenizer # See https://pypi.python.org/pypi/pyvi
elif lcode == 'th':
    import pythai # See https://pypi.python.org/pypi/pythai
# elif lcode == 'ar':
#     os.environ['CLASSPATH'] = "../stanford-segmenter-2015-12-09"
#     from nltk.tokenize.stanford_segmenter import StanfordSegmenter
#     segmenter = StanfordSegmenter(path_to_jar="../stanford-segmenter-2015-12-09/stanford-segmenter-3.6.0.jar",
#                                path_to_sihan_corpora_dict="../stanford-segmenter-2015-12-09/data",
#                                path_to_model="../stanford-segmenter-2015-12-09/data/pku.gz",
#                                path_to_dict="../stanford-segmenter-2015-12-09/data/dict-chris6.ser.gz")

max_corpus_size = args.max_corpus_size
fname = "{}wiki-{}-pages-articles-multistream.xml".format(lcode, DUMP_DATE)

def clean_text(text):
    global lcode

    # Common
    text = regex.sub("(?s)<ref>.+?</ref>", "", text) # remove reference links
    text = regex.sub("(?s)<[^>]+>", "", text) # remove html tags
    text = regex.sub("&[a-z]+;", "", text) # remove html entities
    text = regex.sub("(?s){{.+?}}", "", text) # remove markup tags
    text = regex.sub("(?s){.+?}", "", text) # remove markup tags
    text = regex.sub("(?s)\[\[([^]]+\|)", "", text) # remove link target strings
    text = regex.sub("(?s)\[\[([^]]+\:.+?]])", "", text) # remove media links

    text = regex.sub("[']{5}", "", text) # remove italic+bold symbols
    text = regex.sub("[']{3}", "", text) # remove bold symbols
    text = regex.sub("[']{2}", "", text) # remove italic symbols

    if lcode in ['ko']: # korean
        text = regex.sub(u"[^ \r\n\p{Hangul}.?!]", " ", text) # Replace unacceptable characters with a space.
    elif lcode in ['ja']: # japanese
        text = regex.sub(u"[^\r\n\p{Han}\p{Hiragana}\p{Katakana}ー。！？]", "", text)
    elif lcode in ['zh']: # chinsese
        text = regex.sub(u"[^\r\n\p{Han}。！？]", "", text)
    elif lcode in ['th']: # thai
        text = regex.sub(u"[^ \r\n\p{Thai}.?!]", " ", text)
    elif lcode in ['ru']: # russian
        text = regex.sub(u"[^ \r\n\p{Cyrillic}.?!\-]", " ", text)
        text = text.lower()
#     elif lcode in ['ar']: # arabic
#         text = regex.sub(u"[^ \r\n\p{Arabic}.?!\-]", " ", text)
    elif lcode in ['hi']: # hindi
        text = regex.sub(u"[^ \r\n\p{Devanagari}.।?!\-]", " ", text)
    elif lcode in ['bn']: # bengali
        text = regex.sub(u"[^ \r\n\p{Bengali}.।?!\-]", " ", text)
    elif lcode in ['de']: # german
        text = regex.sub(u"[^ \r\n\p{Latin}\-'‘’.?!]", " ", text)
    else: # Mostly european languages
        text = regex.sub(u"[^ \r\n\p{Latin}\-'‘’.?!]", " ", text)
        text = text.lower()

    # Common
    text = regex.sub("[ ]{2,}", " ", text) # Squeeze spaces.
    return text

def sentence_segment(text):
    '''
    Args:
      text: A string. A unsegmented paragraph.

    Returns:
      A list of sentences.
    '''
    global lcode
    if lcode in ['ja', 'zh']:
        sents = regex.split(u"([。！？])?[\n]+|[。！？]", text)
    elif lcode in ['th']:
        sents = text.split("[\n]+")
    elif lcode in ['hi', 'bn']: # hindi, bengali
        sents = regex.split(u"([.।?!])?[\n]+|[.।?!] ", text)
    elif lcode in ['de']: # german
        sents = regex.split("([.?!])?[\n]+|[.?!] ", text)
        sents = [sent[0].lower() + sent[1:] for sent in sents if sent is not None and len(sent) > 1]
    else:
        sents = regex.split("([.?!])?[\n]+|[.?!] ", text)
    return sents

def word_segment(sent):
    '''
    Args:
      sent: A string. A sentence.

    Returns:
      A list of words.
    '''
    global lcode, ST

    if sent is None:
        return sent

    if lcode in ['ko']:
        words = [word for word, _ in kkma.pos(sent)]
    elif lcode in ['ja']:
        words = mecab.parse(sent.encode('utf8')).split()
    elif lcode in ['th']:
        words = pythai.split(sent)
    elif lcode in ['vi']:
        words = ViTokenizer.tokenize(sent).split()
    elif lcode in ['zh']:
        words = list(jieba.cut(sent, cut_all=False))
#     elif lcode in ['ar']:
#         words = segmenter.segment(sent).split()
    else: # Mostly european languages
        words = sent.split()

    words = ST.tokenize(words)

    return words

fout = None

def build_text(text):
    global fout
    if not np.random.binomial(n=1, p=part):
        return
    try:
        text = clean_text(text)
        sents = sentence_segment(text)
        sents = [word_segment(sent) for sent in sents]
        sents = [sent for sent in sents if sent is not None and len(sent) > 10]
        for words in sents:
            fout.write(" ".join(words) + "\n")
    except:
        return


def build_corpus():
    global lcode, max_corpus_size, fname, fout
    from joblib import Parallel, delayed
    from tqdm import tqdm


    ns = "{http://www.mediawiki.org/xml/export-0.10/}" # namespace
    with codecs.open("data/{}.txt".format(lcode), 'w', 'utf-8') as _fout:
        fout = _fout
        with Parallel(n_jobs=workers) as parallel:
            texts = parallel(delayed(build_text)(elem.text)
    for _, elem in tqdm(ET.iterparse("data/{}".format(fname), tag=ns+"text")))


if __name__ == "__main__":
    build_corpus()

    print("Done")
