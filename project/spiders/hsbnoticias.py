import scrapy
from scrapy.loader import ItemLoader
from project.items import News
from project.spiders.simple_spider import SimpleSpider


class HSBNoticiasSpider(SimpleSpider):
    name = "hsbnoticias"
    baseUrl = 'https://hsbnoticias.com/noticias/judicial'

    urlsPath  = '//div[contains(@about, "judicial")]/@about'
    datesPath = '//div[contains(@about, "judicial")]//div[@class="field-items"]/div[@class="field-item"]/text()'
    nextPagePath =  '//li[@class="pager-next"]/a/@href'

    tituloPath = '//div[contains(@about, "judicial")]//div[@class="field-item"]/h2/a/text()'
    cuerpoPath =  '//div[contains(@about, "judicial")]//div[@class="field-item even"]/p/strong/text() | //div[contains(@about, "judicial")]//div[@class="field-item even"]/p/text()'
    fechaPath  = '//div[contains(@about, "judicial")]//div[@class="field-item"]/text()'

    def format_fecha(self, fecha):
      return fecha[:19]
