# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import psycopg2


class CatePipeline(object):

    def open_spider(self, spider):
        hostname = 'localhost'
        username = 'kayn'
        password = 'starvn66' # your password
        database = 'ComicCrawler'
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.cur.execute("insert into Category(categoryName,categoryLink) values(%s,%s)",(item['categoryName'],item['categoryLink']))
        self.connection.commit()
        return item