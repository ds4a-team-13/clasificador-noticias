import scrapy
from scrapy.loader import ItemLoader
from project.items import News
from project.spiders.base_spyder import BaseSpider
import csv
import sqlite3, os 

class ClassifiedNewsSpider(BaseSpider):
    name = 'classified'
    
    def __init__(self, monitor='', **kwargs):
      self.parsers = {
        'minuto30' : self.parse_minuto30,
        'elcolombiano' : self.parse_elcolombiano,
        'caracol' : self.parse_caracol,
        'diariodelsur' : self.parse_diariodelsur,
        'alertapaisa' : self.parse_alertapaisa,
      }


    def clean_url(self, url):
      return url.replace('https://', '')\
                .replace('http://', '')\
                .replace('www.', '')\
                .split('/')[0]\
                .split('.')[0]

    def start_requests(self):

        with open('news.csv', newline='') as f:
          reader = csv.reader(f)
          for row in reader:
            if row[0] == 'category': continue # header line

            cat, url = row[0].strip(), row[1].strip()
            diario = self.clean_url(url) 
            
            if diario in self.parsers:
              yield scrapy.Request(url=url, callback=self.parsers[diario], 
                                  headers=self.headers, meta={'category': cat})

    def read_news(self, response, title_path, body_path):
      category   = response.meta['category']
      diario     = self.clean_url(response.url)

      titulo = response.xpath(title_path).get()
      cuerpo = response.xpath(body_path).getall()
      cuerpo = " ".join(cuerpo)

      self.store_news(titulo, cuerpo, diario, response.url, category)


    def parse_minuto30(self, response):
      title_path = '//div[@class="tittle-nota"]/h1/text()'
      body_path  = '//div[@class="contenttext"]/p//text()'
      self.read_news(response, title_path, body_path)
    

    def parse_elcolombiano(self, response):
      title_path = '//h3[@class="headline"]/span/text()'
      body_path  = '//div[@class="noticia"]/article/p//text()'
      self.read_news(response, title_path, body_path)
      
    
    def parse_caracol(self, response):
      title_path = '//h1[@itemprop="headline"]/text()'
      body_path  = '//div[@class="cuerpo"]/p//text()'
      self.read_news(response, title_path, body_path)
    
    def parse_diariodelsur(self, response):
      title_path = '//div[@id="block-system-main"]/div[@class="content"]//h2//text()'
      body_path  = '//div[@id="block-system-main"]/div[@class="content"]//p/text()'
      self.read_news(response, title_path, body_path)

    def parse_alertapaisa(self, response):
      title_path = '//div[@class="node-header"]//h1/span/text()'
      body_path  = '//div[@class="content col-md-8"]//p//text()'
      self.read_news(response, title_path, body_path)
    
    def store_news(self, titulo, cuerpo, diario, url, category):
      path = os.path.dirname(os.path.abspath(__file__))
      db_path = path + '/../../data.db'

      conn = sqlite3.connect(db_path)
      cursor = conn.cursor()

      cursor.execute('INSERT INTO classified_news VALUES (?,?,?,?,?)', 
            (titulo, cuerpo, diario, url, category))

      conn.commit()
      conn.close()


              


