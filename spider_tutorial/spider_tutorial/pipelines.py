# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import pymongo
import sqlite3


class MongodbPipeline:
    collection_name = 'transcripts'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(
            "mongodb+srv://sloboda282:qwerty0192@cluster0.rh3h4tf.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client['My_Database']

    def close_spider(self, spider):
        self.client.close()


class SQLitePipeline:

    def open_spider(self, spider):
        self.connection = sqlite3.connect('audible.db')
        self.c = self.connection.cursor()
        self.c.execute('''
            CREATE TABLE audible(
            title TEXT,
            author TEXT,
            length TEXT,
            ''')
        self.connection.commit()

    def process_item(self, item, spider):
        self.c.execute("""INSERT INTO audible (title, author, length) VALUES(?,?,?)""",
                       (item.get('title'), item.get('author'), item.get('length'),))
        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.client.close()


class SpiderTutorialPipeline:
    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item
