from nltk.stem.snowball import RussianStemmer, EnglishStemmer


class SentenceTokenizer(object):
	def __init__(self, lang, make_delimiters=True):
		self.__stemmers = {
			'en': EnglishStemmer(),
			'ru': RussianStemmer(),
		}

		if lang not in ('en', 'ru'):
			raise ValueError

		self.__active_stemmer = self.__stemmers[lang]
		self.__make_delimiters = make_delimiters


	def tokenize(self, sentence):
		tokens = [self.__tokenize_word(word) for word in sentence.split(' ')]

		tokenized_sentence = [_ for token in tokens for _ in token]

		if self.__make_delimiters:
			tokenized_sentence = ['<s>'] + tokenized_sentence + ['<\s>']

		return tokenized_sentence

	def __tokenize_word(self, word):
		stem = self.__active_stemmer.stem(word)
		affix = word[len(stem):]

		if affix:
			return (stem, affix)
		else:
			return (stem, )
