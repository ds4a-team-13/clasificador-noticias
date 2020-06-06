import scrapy
from scrapy.loader import ItemLoader
from project.items import News


class ElNuevoDiaSpider(scrapy.Spider):
    name = "elnuevodia"

    def start_requests(self):
        urls = [
            'http://www.elnuevodia.com.co/nuevodia/actualidad/judicial',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
      container = response.xpath('//div[@class="view-content"]')
      for url in container.xpath('//article//header//a/@href').getall():
        next_page = response.urljoin(url)
        yield scrapy.Request(url=next_page, callback=self.read_news)
      
    def read_news(self, response):
      titulo = response.xpath('//div[@id="block-pagetitle"]//h1/span/text()').get()
      cuerpo = response.xpath('//div[@class="node-content"]//p//text()').getall()
      hora   = response.xpath('//div[@class="node-content"]//time/@datetime').get()

      news = ItemLoader(item=News())
      news.add_value('titulo', titulo)
      news.add_value('cuerpo', cuerpo)
      news.add_value('hora', hora)
      news.add_value('url', response.url)
      news.add_value('diario', self.name)
      return news.load_item()
      