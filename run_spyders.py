from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from project.spiders.eldiario import ElDiarioSpider
from project.spiders.elnuevodia import ElNuevoDiaSpider
from project.spiders.elpais import ElPaisSpider
from project.spiders.hoydiariodelmagdalena import DiarioMagdalenaSpider
from project.spiders.lanacion import LaNacionSpider

configure_logging()
runner = CrawlerRunner(get_project_settings())

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(ElDiarioSpider)
    yield runner.crawl(ElNuevoDiaSpider)
    yield runner.crawl(ElPaisSpider)
    yield runner.crawl(DiarioMagdalenaSpider)
    yield runner.crawl(LaNacionSpider)
    reactor.stop()

crawl()
reactor.run() 