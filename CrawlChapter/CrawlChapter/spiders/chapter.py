# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import csv
from scrapy.shell import inspect_response

class ChapterSpider(scrapy.Spider):
    name = 'chapter'
    allowed_domains = ['nettruyen.com']

    def start_requests(self):
        with open("../../text.csv",newline='') as f:
            read = csv.reader(f)
            line_count = 0
            for row in read:
                if line_count == 0:
                    line_count = 1
                    continue
                else:
                    yield Request(url=row[4],callback=self.parse_list_chapter,meta = {"item":row[0]})

    def parse_list_chapter(self,response):
        last_modify = response.headers.getlist("Date")
        object_id = response.meta.get("item")
        list_chapter = response.xpath("//div[@class = 'col-xs-5 chapter']/a/@href").getall() 
        result = dict()
        result["id"] = object_id
        result["last_modify"] = last_modify
        result["chapters"] = list_chapter
        yield result
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)


