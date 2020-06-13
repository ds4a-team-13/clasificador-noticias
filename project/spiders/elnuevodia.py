import scrapy
from scrapy.loader import ItemLoader
from project.items import News
from project.spiders.simple_spider import SimpleSpider


class ElNuevoDiaSpider(SimpleSpider):
    name = "elnuevodia"
    baseUrl = 'http://www.elnuevodia.com.co/nuevodia/actualidad/judicial?page='

    urlsPath = '//div[@class="view-content"]//article//header//a/@href'
    datesPath = '//div[@class="view-content"]//article//time/@datetime'
    nextPagePath = '//nav//li[@class="pager__item pager__item--last"]/a/@href'

    tituloPath = '//div[@id="block-pagetitle"]//h1/span/text()'
    cuerpoPath = '//div[@class="node-content"]//p//text()'
    fechaPath   = '//div[@class="node-content"]//time/@datetime'
    
    def format_fecha(self, fecha):
      return fecha[:19]
      