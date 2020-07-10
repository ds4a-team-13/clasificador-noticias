import pandas as pd
from datetime import datetime          # Handling of dates
from base64 import b64encode           # Build id per news

def filter_data(df: pd.DataFrame) -> pd.DataFrame:
	"""
	This function filter data from scraper
	"""
	print('process_filter_data...')
	
	df['year'] = df['fecha_publicacion'].str[:4]
	
	# filtering dates out of analysis
	df = df.query('year >= "2012"')
	df = df.query('year != "2999"')
	# cast date
	df['fecha_publicacion'] = pd.to_datetime(df['fecha_publicacion'])
	
	df['month'] = [datetime.strftime(x, '%m') for x in df['fecha_publicacion']]
	# Week number of year, Sunday as the first day of week, 00-53
	df['week'] = [datetime.strftime(x, '%U') for x in df['fecha_publicacion']]
	
	# In order for the id to look actually like a unique identifier, let's use base64 encode to convert the id to a base64 string
	# The command converts the newly created id column into bytes, and then gets the base64 encoded value for the same. 
	# Then the base64 value is converted to string again and then stored in the id column.
	df['id'] = df['url'].apply(lambda x: b64encode(x.encode()).decode())
	df.drop_duplicates(['id'], inplace = True)
	
	# how long is the body per news
	df['long_cuerpo'] = df['cuerpo'].apply(lambda x: len(x.split()))
	
	print('Number of news with 0 words in the body:', sum(df['long_cuerpo'] == 0))
	print('Number of news with less than 10 words in the body:', sum(df['long_cuerpo'] <= 10))
	
	df = df[df['long_cuerpo'] > 10]
	
	print(df.shape)
	
	print('process_filter_data finished')
	
	return df
