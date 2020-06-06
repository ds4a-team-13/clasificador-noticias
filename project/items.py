# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, Join
from scrapy import Field
from datetime import datetime

def text_processor(string):
    return ''.join(string).strip()

def date_processor(date):
    return datetime.strptime(date[0], '%Y-%m-%dT%H:%M:%S')

class News(scrapy.Item):
    titulo = Field(output_processor=TakeFirst())
    cuerpo = Field(output_processor=text_processor)
    fecha_publicacion = Field(output_processor=date_processor)
    url    = Field(output_processor=TakeFirst())
    diario = Field(output_processor=TakeFirst())
