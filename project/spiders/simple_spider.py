import scrapy
from scrapy.loader import ItemLoader
from project.items import News
from project.spiders.base_spyder import BaseSpider


class SimpleSpider(BaseSpider):
    
    def parse(self, response):
      print('parsing: ', response.url)
      
      for url in response.xpath(self.urlsPath).extract():
        next_page = response.urljoin(url)
        yield scrapy.Request(url=next_page, callback=self.read_news)
      
      dates = response.xpath(self.datesPath).extract()
      year = int(dates[-1][:4])

      existsNextPage = response.xpath(self.nextPagePath).extract()
      if year >= self.min_year and existsNextPage:
        self.current_page += 1

        url = self.baseUrl + str(self.current_page)
        yield scrapy.Request(url=url, callback=self.parse)


    def read_news(self, response):
      titulo = response.xpath(self.tituloPath).get()
      cuerpo = response.xpath(self.cuerpoPath).getall()
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
      