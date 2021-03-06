import scrapy
from scrapy.loader import ItemLoader
from project.items import News
from project.spiders.simple_spider import SimpleSpider
import datetime


class LaNacionSpider(SimpleSpider):
    name = "lanacion"
    baseUrl = 'https://www.lanacion.com.co/category/judicial/page/'
    googleUrl = 'https://www.lanacion.com.co/category/judicial/'

    urlsPath  = '//div[@class="penci-pmore-link"]/a/@href'
    datesPath = '//div[@class="entry-meta"]//time/@datetime'
    nextPagePath = '//nav//div/a[@class="next page-numbers"]'

    tituloPath = '//header//h1/text()'
    cuerpoPath = '//article//div/p//text()'
    fechaPath   = '//article//time/@datetime'

    def format_fecha(self, fecha):
      return fecha[:19]

    def parse_list_date(self, dates):
      date = dates[-1]
      return datetime.datetime.fromisoformat(date)
