import pandas as pd
import numpy as np

def ubication_news(x: str, region: str, df_dane):
	"""
	This function search the ubications involved in each new
	
	@input:
		-x     : string contains the news
		-region: string contains if the search is by municipio or departamento
	@return:
		ubication_x: string contains all ubications involved in the news
	"""
#	ubication_x = [ub for ub in df_dane[region] if ub in x.split()]
#	ubication_x = set(ubication_x) - set(['colombia'])
#	ubication_x = list(ubication_x)
#	ubication_x = '|'.join(ubication_x)
	
	# token by words
	split_x = x.split()
	# cast from list to series
	split_x = pd.Series(split_x)
	# filter regions
	ubication_x = split_x[split_x.isin(df_dane[region])]
	
	if region == 'departamento':
		def validation_regions(ubication_x , before_word, word):
			# validation valle del cauca or norte de santander
			idx_reg = ubication_x[ubication_x.isin([word])].index
			idx_reg = list(idx_reg)
			
			
			if len(idx_reg) > 0 and idx_reg[0] > 0:
				id_x_1 = np.array(idx_reg) - 1
				split_x_1 = split_x[id_x_1]
				split_x_1_found = split_x_1[split_x_1.isin([before_word])]
				
				if len(split_x_1_found) > 0:
					ubication_x[split_x_1_found.index + 1] = before_word + ' ' + word
			
			return ubication_x
		
		ubication_x = validation_regions(ubication_x, 
									     before_word = 'norte', 
									     word = 'santander')
		
		ubication_x = validation_regions(ubication_x,
									     before_word = 'valle', 
										 word = 'cauca')
	
	ubication_x = [ub for ub in ubication_x if ub != 'colombia']
	
	# if several regions are mentioned, we choose de most frequent
	if len(set(ubication_x)) > 1:
		conteo_ub = pd.Series(ubication_x).value_counts().sort_values(ascending = False)
		if conteo_ub[0] > 1:
			ubication_x = [conteo_ub.index[0]]
	
	ubication_x = set(ubication_x)
	ubication_x = '|'.join(ubication_x)
	
	ubication_x = ubication_x.replace('valle cauca', 'valle del cauca')
	ubication_x = ubication_x.replace('norte santander', 'norte de santander')
	
	print(region, ubication_x)
	
	return ubication_x

def master_ubication(df: pd.DataFrame) -> pd.DataFrame:
	"""
	This function call the above function and process this
	"""
	print('process_ubication...')
	df_ = df.copy()
	df_dane = pd.read_csv('data/external/dane_municipios_colombia.txt', sep = '|')

	# search municipios and departamentos in each news
	df_['municipios']    = df_['pre_clean_text'].apply(lambda x: ubication_news(x, 'municipio', df_dane))
	df_['departamentos'] = df_['pre_clean_text'].apply(lambda x: ubication_news(x, 'departamento', df_dane))
	
	# if the depto is not found but the minucipio yes
	munis_sindepto = df_[df_['departamentos'] == '']['municipios'].copy()
	munis_sindepto = munis_sindepto.str.split('|')\
					.apply(lambda x:  '|'.join(set(df_dane[df_dane['municipio'].isin(x)]['departamento'])))

	df_.loc[df_['departamentos'] == '', 'departamentos'] = munis_sindepto
	
	print('process_ubication finished')
	
	return df_
