# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# from scrapy.exporters import JsonItemExporter



# class JsonPipeline(object):
#     def __init__(self):
#         self.file = open("1.json", 'wb')
#         self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
#         self.exporter.start_exporting()

#     def close_spider(self, spider):
#         self.exporter.finish_exporting()
#         self.file.close()

#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item


import pymongo
from scrapy.exceptions import DropItem


class MongoDBPipeline(object):
    
    def __init__(self):
        connection = pymongo.MongoClient(
            'localhost',
            27017
        )
        db = connection["ComicCrawlered"]
        self.collection = db["Comic"]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
        return item