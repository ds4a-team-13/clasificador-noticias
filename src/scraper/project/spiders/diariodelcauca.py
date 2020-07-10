import scrapy
from scrapy.loader import ItemLoader
from project.items import News
from project.spiders.simple_spider import SimpleSpider
from datetime import datetime

class DiarioDelCaucaSpider(SimpleSpider):
    name = "diariodelcauca"
    baseUrl = 'https://diariodelcauca.com.co/noticias/judicial?page='
    googleUrl = 'https://diariodelcauca.com.co/noticias/judicial'

    urlsPath  = '//div[starts-with(@class, "node node-article node-reviewed")]//div[@class = "content"]//div[@class = "field-item"]//h2/a/@href'
    nextPagePath = '//div[@class = "content"]//div[@class = "item-list"]/ul//li[@class = "pager-next"]/a/@href'
    datesPath = '//div[starts-with(@class, "node node-article node-reviewed")]//div[@class = "content"]//div[@class="field field-datetime"]//div[@class = "field-item"]/text()' 

    tituloPath  = '//div[@id="block-system-main"]/div/div/div/div[@class="field field-title"]//h2/a/text()'
    cuerpoPath  = '//div[@class = "t-content"]//p//text()'
    cuerpoPath2 = '//div[@class = "t-content"]//div[@class="rtejustify"]//text()'
    cuerpoPath3 = '//div[@class="t-content"]/div/div/div/div/div/div/div/div/div/text()'
    fechaPath   = '//div[@class = "field field-title"]/following-sibling::div[@class="field field-datetime"]//div[@class = "field-item"]/text()'

    def format_fecha(self, fecha):
    
      fecha = fecha.split(',')[-2:]
      month = fecha[0].strip().split()[0]
      month = month.lower()
      day = fecha[0].strip().split()[1]
      
      year = fecha[1].split('-')[0]
      year = year.strip()
      
      hour = fecha[1].split('-')[1]
      hour = hour.strip()
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
      
      fecha = year + '-' + months[month] + '-' + day + 'T' + hour + ':00'
      return fecha
  
    def parse_list_date(self, dates):
      """
      This function process date obtained from datesPath to transform in format need
      
      :params fecha: string date scraped from datesPath in format: DD/MM/YYYY - HH:MM
      :return year: int year of the publication news
      """
      print(dates)
      last_date = dates[-1]
      last_date = last_date.split('-')[0].strip()
      
      return datetime.strptime(last_date, '%d/%m/%Y')
  
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