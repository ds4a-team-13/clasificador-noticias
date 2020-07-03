import scrapy
from scrapy.loader import ItemLoader
from project.items import News
from project.spiders.simple_spider import SimpleSpider
from datetime import datetime

class ElNuevoSigloSpider(SimpleSpider):
    date_pbl_min = datetime.now()
    name = "elnuevosiglo"
    baseUrl = 'https://www.elnuevosiglo.com.co/seccion/nacion?page='

    urlsPath  = '//h2/a/@href'
    nextPagePath = '//a[@class = "button"]/@href'

    tituloPath = '//h1[@class = "page-title"]//span/text()'
    
    cuerpoPath = '//div[@property="schema:text"]//text()'
    fechaPath  = '//div[@class="info-line"][position() = 3]/text()'

    def format_fecha(self, fecha):
      """
        Ejemplo de entrada: '            Junio 27, 2020 - 08:25 PM'
      """
      
      fecha = fecha.strip()
      #print('entrando', fecha)
      fecha = fecha.split(',')
      
      month_day = fecha[0].strip().split()
      year_hour = fecha[1].strip().split('-')
      
      month = month_day[0].strip().lower()
      day   = month_day[1]
      year  = year_hour[0].strip()
      
      months = {"enero": '01',
          "febrero": '02',
          "marzo": '03',
          "abril": '04',
          "mayo": '05',
          "junio": '06',
          "julio": '07',
          "agosto": '08',
          "septiembre": '09',
          "octubre": '10',
          "noviembre": '11',
          "diciembre": '12'}
      
      fecha = year + '-' + months[month] + '-' + day + 'T00:00:00'
      #print('saliendo', fecha)
      return fecha
  
    def parse(self, response):
      print('parsing: ', response.url)

      for url in response.xpath(self.urlsPath).extract():
        next_page = response.urljoin(url)
        yield scrapy.Request(url=next_page, callback=self.read_news)
      
      last_date = self.date_pbl_min
      print('last_date:', last_date)
      year = last_date.year

      existsNextPage = response.xpath(self.nextPagePath).extract()
      
      if year >= self.min_year and existsNextPage:
        self.current_page += 1

        url = self.baseUrl + str(self.current_page)
        yield scrapy.Request(url=url, callback=self.parse)

      elif year > self.min_year and not existsNextPage:
        print('-- Started google search')
        search_url = self.googleUrl if self.googleUrl else self.baseUrl 

        url = "https://www.google.com/search?q=site:{}&num=100&tbs=cdr:1,cd_min:{},cd_max:1/1/{}"
        url = url.format(search_url, last_date.strftime('%m/%d/%Y'), self.min_year)

        yield scrapy.Request(url=url, callback=self.google_parse, headers=self.headers)
        
    def read_news(self, response):
      print('simple_spider: read_news')
      titulo = response.xpath(self.tituloPath).get()
      cuerpo = response.xpath(self.cuerpoPath).getall()
      fecha_publicacion   = response.xpath(self.fechaPath).get()
      
      # Date should has format: YYYY-MM-DDTHH:MM:SS
      fecha_publicacion = self.format_fecha(fecha_publicacion)
      
      if datetime.strptime(fecha_publicacion, '%Y-%m-%dT%H:%M:%S') < self.date_pbl_min:
          self.date_pbl_min = datetime.strptime(fecha_publicacion, '%Y-%m-%dT%H:%M:%S')

      news = ItemLoader(item=News())
      news.add_value('titulo', titulo)
      news.add_value('cuerpo', cuerpo)
      news.add_value('fecha_publicacion', fecha_publicacion)
      news.add_value('url', response.url)
      news.add_value('diario', self.name)
      news.add_value('page', self.current_page)
      return news.load_item()
