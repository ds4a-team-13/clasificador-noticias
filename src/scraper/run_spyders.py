#####
import os
# path of work
ruta = 'D:/Documentos/Sebastian/01_CURSOS_VISTOS/02_CURSOS_ONLINE/202005_DATA_SCIENCE/final_project/clasificador-noticias/data'
os.chdir(ruta)
#####

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings


#from project.spiders.diariodelcauca import DiarioDelCaucaSpider
#from project.spiders.diariodelhuila import DiarioDelHuilaSpider
#from project.spiders.elcolombiano import ElColombianoSpider

#from project.spiders.eldiario import ElDiarioSpider
#from project.spiders.elinformador import ElInformadorSpider
from project.spiders.elnuevodia import ElNuevoDiaSpider
#from project.spiders.elnuevosiglo import ElNuevoSigloSpider
#from project.spiders.elpais import ElPaisSpider
#from project.spiders.elpueblo import ElPuebloSpider
#from project.spiders.hoydiariodelmagdalena import DiarioMagdalenaSpider
#from project.spiders.lanacion import LaNacionSpider
#from project.spiders.laopinion import LaOpinionSpider
#from project.spiders.miputumayo import MiPutumayoSpider
#from project.spiders.hsbnoticias import HsbNoticiasSpider
#from project.spiders.jep import JepSpider

configure_logging()
runner = CrawlerRunner(get_project_settings())

@defer.inlineCallbacks
def crawl():
#    yield runner.crawl(DiarioDelCaucaSpider)
#    yield runner.crawl(DiarioDelHuilaSpider)
#    yield runner.crawl(ElColombianoSpider)
	
#    yield runner.crawl(ElDiarioSpider)
#    yield runner.crawl(ElInformadorSpider)
    yield runner.crawl(ElNuevoDiaSpider)
#    yield runner.crawl(ElNuevoSigloSpider)
#    yield runner.crawl(ElPaisSpider)
#    yield runner.crawl(ElPuebloSpider)
#    yield runner.crawl(DiarioMagdalenaSpider)
#    yield runner.crawl(LaNacionSpider)
#    yield runner.crawl(LaOpinionSpider)
#    yield runner.crawl(MiPutumayoSpider)
#    yield runner.crawl(HsbNoticiasSpider)
#    yield runner.crawl(JepSpider)
    reactor.stop()

crawl()
reactor.run()
