# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class PlaywrightScraperPipeline:
    def process_item(self, item, spider):
        return item

# class SqliteDemoPipeline:
#     def process_item(self, item, spider):
#         return item
    
import sqlite3

class SQLitePipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect('biki_data.db')
        self.c = self.connection.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS biki_products
            (url TEXT, image TEXT, name TEXT, price TEXT)''')

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.c.execute("INSERT INTO biki_products (url, image, name, price) VALUES (?, ?, ?, ?)", (
            item['url'],
            item['image'],
            item['name'],
            item['price']
        ))
        self.connection.commit()
        return item