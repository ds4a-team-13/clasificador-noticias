import pandas as pd
pd.options.display.max_columns = None
import sqlite3
from datetime import datetime          # Handling of dates
from base64 import b64encode           # Build id per news
from nltk.corpus import stopwords      # stopwords from nltk
from stop_words import get_stop_words  # stopwords from scipy
from nltk import SnowballStemmer       # Stemming (word root)
from unidecode import unidecode        # Removal of accents
import es_core_news_sm                 # Tagger model in spanish
import pickle
