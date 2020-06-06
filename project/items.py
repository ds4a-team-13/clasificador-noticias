# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, Join
from scrapy import Field

def text_processor(string):
    return ''.join(string).strip()

class News(scrapy.Item):
    titulo = Field(output_processor=TakeFirst())
    cuerpo = Field(output_processor=text_processor)
    hora   = Field(output_processor=TakeFirst())
    url    = Field(output_processor=TakeFirst())
    diario = Field(output_processor=TakeFirst())
