import pandas as pd
import es_core_news_sm                 # Tagger model in spanish
#from collections import defaultdict

def process_tags_spanish(x: str) -> list:
	"""
	This function extract tags of one string
	@input: 
		x: string that contains text
	@return:
		tags: list of tuples with all tags for each word
	"""
	# nlp model for extract tags
	doc = nlp(x)
	# here we extract the tag for each word and validate if the word is in names file,
	# then is the 'NOUN', in otherwise is the pos_ extract from scipy
	tags = [(w.text, 'NOUN') if w.text in names else (w.text, w.pos_) for w in doc]
	
	#tags_dict = defaultdict(list)
	#for text, tag in tags:
	#	tags_dict[tag].append(text)
	
	return tags

def master_tags_spanish(serie_word: pd.Series) -> pd.Series:
	"""
	This function apply the above function to each news
	
	@input:
		serie_word: series object contains all news text
	@return:
		tags_pos: dictionary that contains the id of news in the keys and the 
		          list of tuples with tags_pos in the values
	"""	
	# model for tags in spanish from scipy
	nlp = es_core_news_sm.load()
	# names file
	df_names = pd.read_csv('data/external/stopwords_names.txt')
	names = list(df_names['name'])
	
	# applying the above function to each text
	tags_pos = serie_word.apply(process_tags_spanish)
	
	return tags_pos
	
	