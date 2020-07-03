import scrapy
from scrapy.loader import ItemLoader
from project.items import News
from project.spiders.simple_spider import SimpleSpider
import datetime

class ElPuebloSpider(SimpleSpider):
    name = "elpueblo"
    baseUrl = 'http://elpueblo.com.co/category/noticias/page/'

    urlsPath  = '//div[@class = "column half"]//h2//a/@href'
    nextPagePath = '//a[@class="next page-numbers"]/@href'
    datesPath = '//div[@class = "column half"]//time/@datetime' 

    tituloPath = '//header//h1/text()'
    cuerpoPath = '//div[@class="post-content text-font description"]//p/text()'
    cuerpoPath2 = '//div[@class="post-content text-font description"]//*[@style="text-align: justify;"]/text()'
    cuerpoPath3 = '//div[@class="post-content text-font description"]//span/text()'
    fechaPath   = '//div[@class = "post-meta"]//span[@class="dtreviewed"]/time/@datetime'

    def format_fecha(self, fecha):
      return fecha[:19]

    def parse_list_date(self, dates):
      """
      This function process date obtained from datesPath to transform in format need
      
      :params fecha: string date scraped from datesPath in format: YYYY-MM-DDTHH:MM:SS
      :return year: int year of the publication news
      """
      print(dates)
      last_date = dates[-1]
      
      return datetime.datetime.fromisoformat(last_date)

    def read_news(self, response):
      print('read_news spider')
      titulo = response.xpath(self.tituloPath).get()
      try:
          cuerpo = response.xpath(self.cuerpoPath).getall()
      except:
          try:
              cuerpo = response.xpath(self.cuerpoPath2).getall()
          except:
              cuerpo = response.xpath(self.cuerpoPath3).getall()

      fecha_publicacion   = response.xpath(self.fechaPath).get()
      
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
  