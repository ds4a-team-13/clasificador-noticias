import scrapy
from scrapy.loader import ItemLoader
from project.items import News


class LaNacionSpider(scrapy.Spider):
    name = "lanacion"

    def start_requests(self):
        urls = [
            'https://www.lanacion.com.co/category/judicial/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
      container = response.xpath('//div[@class="penci-archive__list_posts"]')
      for url in container.xpath('//article//div[@class="penci-pmore-link"]/a/@href').getall():
        yield scrapy.Request(url=url, callback=self.read_news)
      
    def read_news(self, response):
      titulo = response.xpath('//header//h1/text()').get()
      cuerpo = response.xpath('//article//div/p/text()').getall()
      hora   = response.xpath('//article//time/@datetime').get()
      
      news = ItemLoader(item=News())
      news.add_value('titulo', titulo)
      news.add_value('cuerpo', cuerpo)
      news.add_value('hora', hora)
      news.add_value('url', response.url)
      news.add_value('diario', self.name)
      return news.load_item()