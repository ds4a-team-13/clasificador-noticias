import scrapy
from scrapy.loader import ItemLoader
from project.items import News
from project.spiders.base_spyder import BaseSpider


class SimpleSpider(BaseSpider):

    def parse(self, response):
      print('response:', response)
      print('parsing: ', response.url)

      for url in response.xpath(self.urlsPath).extract():
        print('url:', url)
        next_page = response.urljoin(url)
        yield scrapy.Request(url=next_page, callback=self.read_news)
      
      dates = response.xpath(self.datesPath).extract()
      #last_date = self.parse_list_date(dates[-1].strip())
      last_date = self.parse_list_date(dates)
      year = last_date.year

      existsNextPage = response.xpath(self.nextPagePath).extract()
      
      if year >= self.min_year and existsNextPage:
        self.current_page += 1

        url = self.baseUrl + str(self.current_page)
        yield scrapy.Request(url=url, callback=self.parse)

      elif  year > self.min_year and not existsNextPage:
        print('-- Started google search')
        search_url = self.googleUrl if self.googleUrl else self.baseUrl 

        url = "https://www.google.com/search?q=site:{}&num=100&tbs=cdr:1,cd_min:{},cd_max:1/1/{}"
        url = url.format(search_url, last_date.strftime('%m/%d/%Y'), self.min_year)

        yield scrapy.Request(url=url, callback=self.google_parse, headers=self.headers)
        

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


    def google_parse(self, response):
      # This is an indicator to show that the news was obtained from google
      self.current_page = -1

      urls = response.xpath('//div[@class="rc"]//div[@class="r"]/a/@href').extract()
      for url in urls:
        yield scrapy.Request(url=url, callback=self.read_news)

      next_page = response.xpath('//a[@id="pnnext"]/@href').get()
      if next_page:
          url = response.urljoin(next_page)
          yield scrapy.Request(url=url, callback=self.google_parse)


    def parse_list_date(self, date):
      """
        This method is intended to be defined in each subclass to 
        return a datetime object
      """
      return date      