# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from Category.helpers.category_item import CategoryItem
from w3lib.html import remove_tags


class CategoriesSpider(scrapy.Spider):
    name = 'Categories'
    allowed_domains = ['nettruyen.com']
    start_urls = ['http://www.nettruyen.com/tim-truyen']

    def start_requests(self):
        for i in self.start_urls:
            yield Request(url=i,callback = self.parse_category)

    def parse_category(self,response):
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)
        name = list(map(remove_tags,response.xpath("//div[@class = 'ModuleContent']/ul[@class = 'nav']/li[not(contains(@class, 'active'))]").getall()))
        name = list(map(lambda x:x.strip(),name))
        link = list(response.xpath("//div[@class = 'ModuleContent']/ul[@class = 'nav']/li[not(contains(@class, 'active'))]/a/@href").getall())
        list_category_item = list()
        for i in range(len(name)):
            list_category_item.append(CategoryItem(name[i],link[i]))
        list_items = list(map(lambda x:x.__dict__,list_category_item))
        for i in list_items:
            yield i
    