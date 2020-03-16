# -*- coding: utf-8 -*-
import scrapy
import psycopg2
from scrapy import Request
from time import gmtime, strftime
from w3lib.html import remove_tags
from ComicCategoryItem.helpers.comic import Comic
from scrapy.linkextractors import LinkExtractor

class CategoryitemSpider(scrapy.Spider):
    name = 'CategoryItem'
    allowed_domains = ['nettruyen.com']

    def start_requests(self):
        connection = psycopg2.connect(user="kayn",password="starvn66",host="localhost",port="5432",database="ComicCrawler")
        
        cursor = connection.cursor()
        postgreSQL_select_Query = "select * from Category"

        cursor.execute(postgreSQL_select_Query)
        records = cursor.fetchall() 
        cursor.close()
        connection.close() 
        for item in records:
            yield Request(url=item[2],callback= self.parse_list_Comic,meta = {"item":item[0]})
    
        
    def parse_list_Comic(self,response):
        cate_id = response.meta.get("item")
        last_modified = response.headers.getlist("Date")[0].decode("ASCII")
        last_update = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        intro_images = list(response.xpath("//div[@class ='ModuleContent']/div[@class ='items']/div[@class = 'row']/div[@class = 'item']/figure[@class ='clearfix']/div[@class ='image']/a/img/@data-original").getall())
        intro_title = response.xpath("//div[@class ='ModuleContent']/div[@class ='items']/div[@class = 'row']/div[@class = 'item']/figure[@class ='clearfix']/figcaption/h3/a").getall()
        intro_titles = list(map(remove_tags,intro_title))
        intro_links = list(map(remove_tags,response.xpath("//div[@class ='ModuleContent']/div[@class ='items']/div[@class = 'row']/div[@class = 'item']/figure[@class ='clearfix']/figcaption/h3/a/@href").getall()))
        name = list(map(remove_tags,response.xpath("//div[@class ='ModuleContent']/div[@class ='items']/div[@class = 'row']/div[@class = 'item']/figure[@class ='clearfix']/figcaption/h3/a").getall()))  
        for i in range(len(intro_links)):
            yield Comic(cate_id,last_modified,last_update,intro_links[i],intro_images[i],name[i]).__dict__

        next_page = LinkExtractor(restrict_xpaths="//div[@class = 'pagination-outter']/ul[@class = 'pagination']/li/a[@class = 'next-page']").extract_links(response)
        if next_page is not None:
            yield Request(url = next_page[0].url,callback=self.parse_list_Comic,meta = {"item":cate_id})