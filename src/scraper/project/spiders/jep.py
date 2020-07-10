import scrapy
from scrapy.loader import ItemLoader
from project.items import News
from project.spiders.base_spyder import BaseSpider
from bs4 import BeautifulSoup
import locale 
import datetime 
import csv
locale.setlocale(locale.LC_TIME, '')

class JepSpider(BaseSpider):
    name = 'jep'

    def start_requests(self):
        max_date = datetime.datetime.now()
        date = datetime.datetime(2020, 3, 25)

        baseUrl = 'https://pinvestigacion123.wixsite.com/bitacoraseidora/{}'
        urls = []

        while(date < max_date):
          urls.append(baseUrl.format(date.strftime('%-d-de-%B-%Y') ))
          urls.append(baseUrl.format(date.strftime('%-d-de-%B-de-%Y') ))
          date += datetime.timedelta(days=1)
        
        print('url, category')
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)
            

    def parse(self, response):
      path = '//div[@id="PAGES_CONTAINERinlineContent"]/div/div/div[2]/div/div/div'
      divs = response.xpath(path).getall()
      
      for div in divs[1:]:
        soup = BeautifulSoup(div, 'html.parser')
        
        categoryBlock = soup.find_all('h2')
        if categoryBlock:
          category = soup.h2.get_text()
        
        news = soup.find_all('p')
        if news:
          for a in soup.find_all('a'):
            if a.get_text() == "Ver noticia":
              url = a['href']
              print(category, ', ', url)
              


