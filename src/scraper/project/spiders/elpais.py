import scrapy
from scrapy.loader import ItemLoader
from project.items import News
from project.spiders.simple_spider import SimpleSpider
import datetime


class ElPaisSpider(SimpleSpider):
    name = "elpais"
    baseUrl = 'https://www.elpais.com.co/page/lista-de-notas-judicial.html?page='
    googleUrl = 'www.elpais.com.co/judicial'
    
    urlsPath  = '//div[contains(@class, "listing-item")]//h2//a/@href'
    datesPath = '//div[contains(@class, "listing-item")]//span[@class="schemeArticle"]/meta[@itemprop="dateModified"]/@content'
    nextPagePath = '//a[@rel="next"]'
    
    tituloPath = '//div[@class="article-top row"]//h1/text()'
    cuerpoPath = '//div[@class="article-content"]//p/text()'
    fechaPath  = '//meta[@name="cXenseParse:recs:publishtime"]/@content'
        

    def format_fecha(self, fecha):
      return fecha+'T00:00:00'

    def parse_list_date(self, dates):
      date = dates[-1]
      return datetime.datetime.strptime(date, '%Y-%m-%d')
    
      