import scrapy
from scrapy.loader import ItemLoader
from project.items import News
from project.spiders.simple_spider import SimpleSpider
import datetime


class ElColombianoSpider(SimpleSpider):
    name = "elcolombiano"
    baseUrl = 'https://www.elcolombiano.com/cronologia/noticias/meta/judicial#.p:'
    googleUrl = 'www.elpais.com.co/judicial'
    
    urlsPath  = '//div[@class="right"]/a/@href'
    datesPath = '//div[@class="left"]//span/text()'
    nextPagePath = '//*[@id="_2156106677_pagtool2"]/following::li[1]/@data-page'
    
    tituloPath = '//div[@class="information-noticia"]/h3/span/text() | //div[@class="left"]/h4/span/text()'
    cuerpoPath = '//article[contains(@class, "fontChange")]/p/text() | //div[@class="left"]/p/text()'
    fechaPath  = '//div[@class="autor"]/h6/text() | //div[@class="tools-video"]/p/text()'
        

    def format_fecha(self, fecha):
      print(fecha)
      try:
          if(type(fecha) == list and len(fecha)>1):
            fecha = fecha[1]
          else:
            if(type(fecha) == list and len(fecha)>1):
                fecha = fecha[0]
                
          if('/' in fecha):
            return datetime.datetime.strptime(fecha[0].replace(" ",""), '%d/%m/%Y')

          fecha = fecha.split(sep="Publicado el ")[1].rstrip().split(sep=" de ")
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
          fecha = fecha[2] + '-' + months[fecha[1]] + '-' + fecha[0]
      except:
          fecha = "2999-01-01"
      
      return fecha+'T00:00:00'

    def parse_list_date(self, date): 
      return datetime.datetime.strptime(date[-1].replace(" ",""), '%d/%m/%Y')