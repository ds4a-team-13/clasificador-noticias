import scrapy
from scrapy.loader import ItemLoader
from project.items import News
from project.spiders.simple_spider import SimpleSpider
from datetime import datetime

class HsbNoticiasSpider(SimpleSpider):
    name = "hsbnoticias"
    baseUrl = 'https://hsbnoticias.com/noticias/judicial?page='

    urlsPath  = '//div[contains(@about, "judicial")]/@about'
    datesPath = '//div[contains(@about, "judicial")]//div[@class="field-items"]/div[@class="field-item"]/text()'
    nextPagePath =  '//li[@class="pager-next"]/a/@href'

    tituloPath = '//div[contains(@about, "judicial")]//div[@class="field-item"]/h2/a/text()'
    cuerpoPath =  '//div[contains(@about, "judicial")]//div[@class="field-item even"]/p/strong/text() | //div[contains(@about, "judicial")]//div[@class="field-item even"]/p/text()'
    fechaPath  = '//div[contains(@about, "judicial")]//div[@class="field-item"]/text()'

    def format_fecha(self, fecha):
    
      fecha = fecha.split(',')[-2:]
      month = fecha[0].strip().split()[0]
      
      day = fecha[0].strip().split()[1]
      
      year = fecha[1].split('-')[0]
      year = year.strip()
      
      hour = fecha[1].split('-')[1]
      hour = hour.strip()
      months = {"Enero": '01',
          "Febrero": '02',
          "Marzo": '03',
          "Abril": '04',
          "Mayo": '05',
          "Junio": '06',
          "Julio": '07',
          "Agosto": '08',
          "Septiembre": '09',
          "Octubre": '10',
          "Noviembre": '11',
          "Diciembre": '12'}
      
      fecha = year + '-' + months[month] + '-' + day + 'T' + hour + ':00'
      return fecha
  
    def parse_list_date(self, date): 
      return datetime.strptime(date[-1].split(' - ')[0], '%d/%m/%Y')