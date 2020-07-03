import scrapy
from scrapy.loader import ItemLoader
from project.items import News
from project.spiders.simple_spider import SimpleSpider
import datetime


class DiarioMagdalenaSpider(SimpleSpider):
    name = "hoydiariodelmagdalena"
    baseUrl = 'http://www.hoydiariodelmagdalena.com.co/archivos/category/judicial/page/'
    googleUrl = 'http://www.hoydiariodelmagdalena.com.co/ + "judicial"'

    urlsPath = '//div[contains(@class, "listing")]//article//h2/a/@href'
    datesPath = '//div[contains(@class, "listing")]//article//div[@class="post-meta"]//time/@datetime'
    nextPagePath = '//div[contains(@class, "pagination")]//div[@class="older"]/a'

    tituloPath = '//article//h1[@class="single-post-title"]/span//text()'
    fechaPath   = '//article//span[@class="time"]/time/@datetime'
    
    def format_fecha(self, fecha):
      return fecha[:19]

    def parse_list_date(self, dates):
      date = dates[-1]
      return datetime.datetime.fromisoformat(date)

    def read_news(self, response):
      cuerpoPaths = [
        '//div[contains(@class,"entry-content")]//*[@style="text-align: justify;"]//text()',
        '//div[contains(@class,"entry-content")]//p//text()',
      ]

      titulo = response.xpath(self.tituloPath).get()
      fecha_publicacion   = response.xpath(self.fechaPath).get()

      for path in cuerpoPaths:
        cuerpo = response.xpath(path).getall()
        if cuerpo: break # Change until find one that works

      
      # Date should has format: YYYY-MM-DDTHH:MM:SS
      fecha_publicacion = self.format_fecha(fecha_publicacion)

      news = ItemLoader(item=News())
      news.add_value('titulo', titulo)
      news.add_value('cuerpo', cuerpo)
      news.add_value('fecha_publicacion', fecha_publicacion)
      news.add_value('url', response.url)
      news.add_value('diario', self.name)
      news.add_value('page', self.current_page)



      return news.load_item()
      