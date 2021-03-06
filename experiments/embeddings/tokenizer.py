from nltk.stem.snowball import RussianStemmer, EnglishStemmer

class SentenceTokenizer(object):
	'''
	Tokenizes sentences using SnowBall Stemmer
	(each word is split into stem and suffix deterministically)
	'''
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
		tokens = [self.__tokenize_word(word) for word in sentence]

		tokenized_sentence = [_ for token in tokens for _ in token]

		if self.__make_delimiters:
			tokenized_sentence = ['<s>'] + tokenized_sentence + ['<\s>']

		return tokenized_sentence


	def detokenize(self, tokens):
		source_text = ''
		for token in tokens:
			source_text += self.__detokenize_token(token)

		return source_text.lstrip()


	def __tokenize_word(self, word):
		stem = self.__active_stemmer.stem(word)
		affix = word[len(stem):]

		if affix:
 			return (stem, '#' + affix)			#To make embeddings work, all suffixes start with artificial token '#'
		else:
			return (stem, )


	def __detokenize_token(self, token):
		if token.startswith('#'):
			return token[1:]
		else:
			return ' ' + token 

