# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class News(scrapy.Item):
    titulo = scrapy.Field()
    cuerpo = scrapy.Field()
    hora   = scrapy.Field()
    
