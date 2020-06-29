import scrapy
from scrapy.loader import ItemLoader
from project.items import News
from project.spiders.simple_spider import SimpleSpider
from datetime import datetime

class MiPutumayoSpider(SimpleSpider):
    name = "miputumayo"
    baseUrl = 'https://miputumayo.com.co/page/{}/?s=judicial'

    urlsPath  = '//h2[@class="entry-title"]//a/@href'
    nextPagePath = '//a[@class="next page-numbers"]/@href'
    datesPath = '//div[@class="entry-meta"]//time[@class="entry-date published"]/@datetime'

    tituloPath = '//header//h1/text()'
    cuerpoPath  = '//div[@class="entry-content"]//p/text()'
    #cuerpoPath2 = '//div[@class="entry-content"]//p/span/text()'
    fechaPath  = '//span[@class="posted-on"]//time/@datetime'

    def format_fecha(self, fecha):
      return fecha[:19]

    def parse_list_date(self, dates):
      """
      This function process date obtained from datesPath to transform in format need
      
      :params fecha: string date scraped from datesPath in format: YYYY-MM-DDTHH:MM:SS
      :return year: int year of the publication news
      """
      print(dates)
      last_date = dates[-1]
      
      return datetime.fromisoformat(last_date)
  
    def start_requests(self):
        self.current_page = self.last_page
        
        urls = [
            self.baseUrl.format(str(self.current_page)),
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)
            
            
    def parse(self, response):
      print('parsing: ', response.url)

      for url in response.xpath(self.urlsPath).extract():
        next_page = response.urljoin(url)
        yield scrapy.Request(url=next_page, callback=self.read_news)
      
      dates = response.xpath(self.datesPath).extract()
      #last_date = self.parse_list_date(dates[-1].strip())
      last_date = self.parse_list_date(dates)
      year = last_date.year

      existsNextPage = response.xpath(self.nextPagePath).extract()
      
      if year >= self.min_year and existsNextPage:
        self.current_page += 1

        url = self.baseUrl.format(str(self.current_page))
        yield scrapy.Request(url=url, callback=self.parse)

      elif year > self.min_year and not existsNextPage:
        print('-- Started google search')
        search_url = self.googleUrl if self.googleUrl else self.baseUrl 

        url = "https://www.google.com/search?q=site:{}&num=100&tbs=cdr:1,cd_min:{},cd_max:1/1/{}"
        url = url.format(search_url, last_date.strftime('%m/%d/%Y'), self.min_year)

        yield scrapy.Request(url=url, callback=self.google_parse, headers=self.headers)