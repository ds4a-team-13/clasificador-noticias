import pandas as pd

def ubication_news(x: str, region: str):
	"""
	This function search the ubications involved in each new
	
	@input:
		-x     : string contains the news
		-region: string contains if the search is by municipio or departamento
	@return:
		ubication_x: string contains all ubications involved in the news
	"""
	ubication_x = [ub for ub in df_dane[region] if ub in x.split()]
	ubication_x = set(ubication_x) - set(['colombia'])
	ubication_x = list(ubication_x)
	ubication_x = '|'.join(ubication_x)
	print(region, ubication_x)
	
	return ubication_x

def master_ubication(df: pd.DataFrame) -> pd.DataFrame:
	"""
	This function call the above function and process this
	"""
	print('process_ubication...')
	
	df_dane = pd.read_csv('data/external/dane_municipios_colombia.txt', sep = '|')

	# search municipios and departamentos in each news
	df['municipios']    = df['pre_clean_text'].apply(lambda x: ubication_news(x, 'municipio'))
	df['departamentos'] = df['pre_clean_text'].apply(lambda x: ubication_news(x, 'departamento'))
	
	print('process_ubication finished')
	
	return df
