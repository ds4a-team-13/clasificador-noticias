import scrapy
from scrapy.loader import ItemLoader
from project.items import News
<<<<<<< HEAD


class ElPaisSpider(scrapy.Spider):
    name = "elpais"
    current_page = 0

    def start_requests(self):
        urls = [
            'https://www.elpais.com.co/judicial',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
      urlsPath = '//div[@class="board-category-secondary"]//div[@class="listing-item "]//h2//a/@href'
      # datesPath = '//div[@class="view-content"]//article//time/@datetime'

      for url in response.xpath(urlsPath).extract():
        print('url:', url)
        # next_page = response.urljoin(url)
        # yield scrapy.Request(url=next_page, callback=self.read_news)

      # dates = response.xpath(datesPath).extract()
      # year = int(dates[-1][:4])
      #
      # if year == 2020:
      #   if 'page' in response.url:
      #     url = response.url[:-1] + str(self.current_page+1)
      #   else:
      #     url = response.url + '?page='+ str(self.current_page+1)
      #
      #   self.current_page = self.current_page + 1
      #   yield scrapy.Request(url=url, callback=self.parse)



    def read_news(self, response):
      titulo = response.xpath('//div[@id="block-pagetitle"]//h1/span/text()').get()
      cuerpo = response.xpath('//div[@class="node-content"]//p//text()').getall()
      fecha_publicacion   = response.xpath('//div[@class="node-content"]//time/@datetime').get()

      # Date should has format: YYYY-MM-DDTHH:MM:SS
      fecha_publicacion = fecha_publicacion[:19]

      news = ItemLoader(item=News())
      news.add_value('titulo', titulo)
      news.add_value('cuerpo', cuerpo)
      news.add_value('fecha_publicacion', fecha_publicacion)
      news.add_value('url', response.url)
      news.add_value('diario', self.name)
      return news.load_item()
=======
from project.spiders.simple_spider import SimpleSpider

class ElPaisSpider(SimpleSpider):
    name = "elpais"
    baseUrl = 'https://www.elpais.com.co/page/lista-de-notas-judicial.html?page='
    
    urlsPath  = '//div[contains(@class, "listing-item")]//h2//a/@href'
    datesPath = '//div[contains(@class, "listing-item")]//span[@class="schemeArticle"]/meta[@itemprop="dateModified"]/@content'
    nextPagePath = '//nav//a[@class="next page-numbers"]'
    
    tituloPath = '//div[@class="article-top row"]//h1/text()'
    cuerpoPath = '//div[@class="article-content"]//p/text()'
    fechaPath  = '//meta[@name="cXenseParse:recs:publishtime"]/@content'
        

    def format_fecha(self, fecha):
      return fecha+'T00:00:00'
    
      
>>>>>>> 9f247d84762b31780fb7f46aaec773cac57e2e5a
