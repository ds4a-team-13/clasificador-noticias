import scrapy
from scrapy.loader import ItemLoader
from project.items import News
from project.spiders.simple_spider import SimpleSpider
import datetime


class ElDiarioSpider(SimpleSpider):
    name = "eldiario"
    baseUrl = 'https://www.eldiario.com.co/categoria/noticias/judicial/page/'
    googleUrl = 'https://www.eldiario.com.co/judicial/'

    
    urlsPath = '//main//article//header/h2/a/@href'
    datesPath = '//main//article//header//span//time/@datetime'
    nextPagePath = '//nav//a[@class="next page-numbers"]'

    tituloPath = '//article//header//h1/text()'
    cuerpoPath = '//main//article//div[@class="entry-content"]/p/text()'
    fechaPath  = '//article//header//time[@class="entry-date published"]/@datetime'

    def format_fecha(self, fecha):
      return fecha[:19]

    def parse_list_date(self, dates):
      date = dates[-1]
      return datetime.datetime.fromisoformat(date)