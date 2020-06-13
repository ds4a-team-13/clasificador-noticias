import scrapy
from scrapy.loader import ItemLoader
from project.items import News
from project.spiders.simple_spider import SimpleSpider


class DiarioMagdalenaSpider(SimpleSpider):
    name = "hoydiariodelmagdalena"
    baseUrl = 'http://www.hoydiariodelmagdalena.com.co/archivos/category/judicial/page/'

    urlsPath = '//div[contains(@class, "listing")]//article//h2/a/@href'
    datesPath = '//div[contains(@class, "listing")]//article//div[@class="post-meta"]//time/@datetime'
    nextPagePath = '//div[contains(@class, "pagination")]//div[@class="older"]/a'

    tituloPath = '//article//h1[@class="single-post-title"]/span/text()'
    cuerpoPath = '//div[contains(@class,"entry-content")]//p/text()'
    fechaPath   = '//article//span[@class="time"]/time/@datetime'
    
    def format_fecha(self, fecha):
      return fecha[:19]
      