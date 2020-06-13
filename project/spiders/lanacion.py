import scrapy
from scrapy.loader import ItemLoader
from project.items import News
from project.spiders.simple_spider import SimpleSpider


class LaNacionSpider(SimpleSpider):
    name = "lanacion"
    baseUrl = 'https://www.lanacion.com.co/category/judicial/page/'

    urlsPath  = '//div[@class="penci-pmore-link"]/a/@href'
    datesPath = '//div[@class="entry-meta"]//time/@datetime'
    nextPagePath = '//nav//div/a[@class="next page-numbers"]'

    tituloPath = '//header//h1/text()'
    cuerpoPath = '//article//div/p/text()'
    fechaPath   = '//article//time/@datetime'

    def format_fecha(self, fecha):
      return fecha[:19]
