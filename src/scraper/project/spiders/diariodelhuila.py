import scrapy
from scrapy.loader import ItemLoader
from project.items import News
from project.spiders.simple_spider import SimpleSpider
import datetime


class DiarioDelHuilaSpider(SimpleSpider):
    name = "diariodelhuila"
    baseUrl = 'https://www.diariodelhuila.com/judicial?page='

    urlsPath = '//div[@class="view-news"]//div[@class="second-news"]//div[@class="view-article"]/a/@href'
    datesPath = '//div[@class="view-news"]//div[@class="second-news"]//div[@class="top-news"]/text()[2]'
    nextPagePath = '//nav//li/a[@class="arrow-pagination pagination-right"]'

    tituloPath = '//div[@class="main-news"]/h1/text()'
    cuerpoPath = '//div[@class="main-news"]/div[@class="text-article"]//text()'
    fechaPath   = '//div[@class="main-news"]/div[@class="top-news"]/text()[2]'
    
    def format_fecha(self, fecha):
      fecha = fecha.strip()[11:21]
      return fecha + 'T00:00:00'
      
  
    def parse_list_date(self, dates):
      date = dates[-1]
      return datetime.datetime.strptime(date, '%Y-%m-%d')

