# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from w3lib.html import remove_tags
from nettruyen.helpers.category_item import CategoryItem
from nettruyen.helpers.comic import Comic
import json
from scrapy.linkextractors import LinkExtractor


class ComicSpider(scrapy.Spider):
    name = 'comic'
    allowed_domains = ['nettruyen.com']
    start_urls = ['http://www.nettruyen.com/tim-truyen']

    def start_requests(self):
        for i in self.start_urls:
            yield Request(url=i,callback = self.parse_category)
    
    def parse_category(self,response):
        name = list(map(remove_tags,response.xpath("//div[@class = 'ModuleContent']/ul[@class = 'nav']/li[not(contains(@class, 'active'))]").getall()))
        name = list(map(lambda x:x.strip(),name))
        link = list(response.xpath("//div[@class = 'ModuleContent']/ul[@class = 'nav']/li[not(contains(@class, 'active'))]/a/@href").getall())
        list_category_item = list()
        for i in range(len(name)):
            list_category_item.append(CategoryItem(name[i],link[i]))
        list_items = list(map(lambda x:x.__dict__,list_category_item))
        for i in list_items:
            yield Request(url = i["link"],callback= self.parse_comic_pagination,meta = {"item":i["name"],"link":i["link"]})
    
    def parse_comic_pagination(self,response):
        name = response.meta.get("item")
        link = response.meta.get("link")
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)
        yield Request(url = link+"?page=1",callback=self.parse_comic_item,meta = {"item":name})
           

    def parse_comic_item(self,response):
        category_name = response.meta.get("item")
        intro_images = list(response.xpath("//div[@class ='ModuleContent']/div[@class ='items']/div[@class = 'row']/div[@class = 'item']/figure[@class ='clearfix']/div[@class ='image']/a/img/@data-original").getall())
        intro_title = response.xpath("//div[@class ='ModuleContent']/div[@class ='items']/div[@class = 'row']/div[@class = 'item']/figure[@class ='clearfix']/figcaption/h3/a").getall()
        intro_titles = list(map(remove_tags,intro_title))
        intro_links = list(map(remove_tags,response.xpath("//div[@class ='ModuleContent']/div[@class ='items']/div[@class = 'row']/div[@class = 'item']/figure[@class ='clearfix']/figcaption/h3/a/@href").getall()))

        for i in range(len(intro_links)):
            yield Comic(intro_titles[i],category_name,intro_images[i],intro_links[i]).__dict__

        next_page = LinkExtractor(restrict_xpaths="//div[@class = 'pagination-outter']/ul[@class = 'pagination']/li/a[@class = 'next-page']").extract_links(response)
        if next_page is not None:
            yield Request(url = next_page[0].url,callback=self.parse_comic_item,meta = {"item":category_name})
        
       

       