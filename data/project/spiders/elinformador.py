import scrapy
from scrapy.loader import ItemLoader
from project.items import News
from project.spiders.simple_spider import SimpleSpider
import datetime


class ElInformadorSpider(SimpleSpider):
    name = "elinformador"
    baseUrl = 'https://www.elinformador.com.co/index.php/judiciales/71-judiciales-local?start='

    urlsPath = '//div[@id="t3-content"]//article//header//a/@href'
    datesPath = '//div[@id="t3-content"]//article//time/@datetime'
    nextPagePath = '//ul[@class="pagination"]//a[@title="Siguiente"]'

    tituloPath = '//article/header/h1/text()'
    fechaPath   = '//article/aside//time/@datetime'
    
    def format_fecha(self, fecha):
      return fecha[:19]

    def parse_list_date(self, dates):
      date = dates[-1]
      return datetime.datetime.fromisoformat(date)

    def read_news(self, response):
      cuerpoPaths = [
        '//article//section[@class="article-content"]//p/text()',
        '//article//section[@class="article-content"]/text()',
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

