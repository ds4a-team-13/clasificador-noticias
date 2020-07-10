import pandas as pd
from nltk.corpus import stopwords      # stopwords from nltk
from stop_words import get_stop_words  # stopwords from scipy
from nltk import SnowballStemmer       # Stemming (word root)
from unidecode import unidecode        # Removal of accents

# function for clean text
def clean_text(serie_word: pd.Series, 
			   stop_words: list,
			   make_stemming: bool) -> pd.Series:
	"""
	This function clean the text: transform to lowercase, removing punctuation,
	removing stopwords, removing accents, removing numbers, stemming words, 
	validate if word is in alphabet and validate if word has more than two letters
	
	@input: 
		-serie_word: serie contains text per news
		-stop_words: list contains stopwords to remove.
		-make_stemming: True if you want to make stemming, False otherwise.
	@return: serie contains clean text per news
	"""
	print('Transform to lowercase...')
	#Lower case
	serie_word = serie_word.str.lower()
	
	print('Removing punctuation...')
	#Removing Punctuation
	serie_word = serie_word.str.replace('[^\w\s]','')
	
	print('Removing accents...')
	#Removal accents
	serie_word = serie_word.apply(lambda x: " ".join(unidecode(word) for word in x.split()))
		
	print('Removing numbers...')
	#Numbers removing
	serie_word = serie_word.str.replace('\d+', '')

	print('Validate if word is in alphabet...')
	serie_word = serie_word.apply(lambda x: " ".join(word for word in x.split() if word.isalpha()))
	
	print('Validate if word has more than two letters...')
	serie_word = serie_word.apply(lambda x: " ".join(word for word in x.split() if len(word) > 2))

	print('Removing stopwords...')
	print('Size list stopwords:', len(stop_words))
	#Removal of Stop Words
	serie_word = serie_word.apply(lambda x: " ".join(word for word in x.split() if word not in stop_words))
	
	if make_stemming:
		print('Stemming words...')
		# Stemming (word root)
		serie_word = serie_word.apply(lambda x: " ".join(spanishstemmer.stem(word) for word in x.split()))
	
	print('Process finished')
	
	return serie_word

def master_clean_text(df: pd.DataFrame) -> pd.DataFrame:
	"""
	This function call the above clean_text function
	"""
	print('process clean_text...')
	
	# stopwords from packages
	stopwords_scipy = get_stop_words('spanish')
	stopwords_nltk  = stopwords.words('spanish')
	
	swords_from_packages = stopwords_scipy + stopwords_nltk
	#Removal of accents in stopwords and lower case
	swords_from_packages = [unidecode(word).lower() for word in swords_from_packages]
	# removal stopwords duplicated
	swords_from_packages = list(set(swords_from_packages))
	print('size words from packages to remove', len(swords_from_packages))
	
	# stop words from file
	df_names = pd.read_csv('data/external/stopwords_names.txt')
	swords_file = list(df_names['name'])
	#Removal of accents in stopwords and lower case
	swords_file = [unidecode(word).lower() for word in swords_file]
	
	# consolidate all stopwords
	swords_all = swords_from_packages + swords_file
	swords_all = list(set(swords_all))
	print('total words dictionary to remove', len(swords_all))
	
	# Stemming (word root)
	spanishstemmer = SnowballStemmer('spanish')
	
	# Applying clean_text function
	df['text'] = df['titulo'] + ' ' + df['cuerpo']
	
	df['pre_clean_text'] = clean_text(serie_word    = df['text'],
									  stop_words    = swords_from_packages,
									  make_stemming = False)
	
	df['clean_text'] = clean_text(serie_word    = df['text'],
								  stop_words    = swords_all,
								  make_stemming = True)
	
	print('process clean_text finished')
	
	return df