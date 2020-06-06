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
      articles = response.xpath('//div[@class="penci-archive__list_posts"]//article')

      urls = response.xpath('//div[@class="penci-pmore-link"]/a/@href').extract()

      for url in urls:
        yield scrapy.Request(url=url, callback=self.read_news)

      dates = response.xpath('//div[@class="entry-meta"]//time/@datetime').extract()
      year = int(dates[-1][:4])
      
      if year == 2020:
        currentPage = response.xpath('//div[@class="nav-links"]//span[@class="page-numbers current"]/text()').get()
        currentPage = int(currentPage)

        if 'page' in response.url:
          url = response.url[:-2] + str(currentPage+1)
        else:
          url = response.url + 'page/2'

        yield scrapy.Request(url=url, callback=self.parse)


    def read_news(self, response):
      titulo = response.xpath('//header//h1/text()').get()

      # In some pages the text is not in <p> tags
      cuerpo = response.xpath('//article//div/p/text()').getall()
      if not cuerpo:
        cuerpo = response.xpath('//article//div[@class="auto"]/text()').getall()

      # Date should has format: YYYY-MM-DDTHH:MM:SS
      fecha_publicacion = response.xpath('//article//time/@datetime').get()
      fecha_publicacion = fecha_publicacion[:19]
      
      news = ItemLoader(item=News())
      news.add_value('titulo', titulo)
      news.add_value('cuerpo', cuerpo)
      news.add_value('fecha_publicacion', fecha_publicacion)
      news.add_value('url', response.url)
      news.add_value('diario', self.name)
      return news.load_item()