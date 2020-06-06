# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import sqlite3
import os

path = os.path.dirname(os.path.abspath(__file__))
db_path = path + '/../data.db'

class FilterPipeline:
    name = 'filterPipeline'

    def open_spider(self, spider):
        
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.cursor.execute('SELECT * FROM news WHERE url = ?', (item['url'],))

        if self.cursor.fetchone():
            raise DropItem("Duplicate item found: %s" % item['url'])
        else:
            return item

class SqlitePipeline:

    def open_spider(self, spider):
        path = os.path.dirname(os.path.abspath(__file__))
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        print(item['titulo'])
        self.cursor.execute('INSERT INTO news VALUES (?,?,?,?,?)', 
            (item['titulo'], item['cuerpo'], item['fecha_publicacion'], item['diario'], 
            item['url']))

        self.conn.commit()

        return item
