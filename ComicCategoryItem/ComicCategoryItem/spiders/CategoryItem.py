# -*- coding: utf-8 -*-
import scrapy
import psycopg2
from scrapy import Request
from datetime import datetime
from w3lib.html import remove_tags
from ComicCategoryItem.helpers.comic import Comic
from scrapy.linkextractors import LinkExtractor

class CategoryitemSpider(scrapy.Spider):
    name = 'CategoryItem'
    allowed_domains = ['nettruyen.com']
    start_urls = ['http://www.nettruyen.com/tim-truyen']

    def start_requests(self):
        # connection = psycopg2.connect(user="kayn",password="starvn66",host="localhost",port="5432",database="ComicCrawler")
        
        # cursor = connection.cursor()
        # postgreSQL_select_Query = "select * from Category"

        # cursor.execute(postgreSQL_select_Query)
        # records = cursor.fetchall() 
        # cursor.close()
        # connection.close() 
        # for item in records:
        #     yield Request(url=item[2],callback= self.parse_list_Comic,meta = {"item":item[0]})
        for i in self.start_urls:
            yield Request(url= i,callback= self.extract_comic_link)
        
    
    def extract_comic_link(self,response):
        items = LinkExtractor(restrict_xpaths = "//div[@class ='ModuleContent']/div[@class ='items']/div[@class = 'row']/div[@class = 'item']/figure[@class ='clearfix']/div[@class ='image']").extract_links(response) 
        for item in items :
            yield Request(url=item.url,callback= self.parse_Comic)  
        next_page = LinkExtractor(restrict_xpaths="//div[@class = 'pagination-outter']/ul[@class = 'pagination']/li/a[@class = 'next-page']").extract_links(response)
        if next_page is not None:
            yield Request(url = next_page[0].url,callback=self.extract_comic_link)
     
        
    def parse_Comic(self,response):
       
        last_modified = response.headers.getlist("Date")[0].decode("ASCII")
        now = datetime.now()
        last_update = now.strftime("%d/%m/%Y %H:%M:%S")
        intro_images = response.xpath("//div[@class = 'detail-info']/div[@class = 'row']/div[@class = 'col-xs-4 col-image']/img/@src").get()   
        comicName = remove_tags(response.xpath("//article/h1[@class ='title-detail']").get()) 
        author = remove_tags(response.xpath("//ul[@class = 'list-info']/li[@class = 'author row']/p[@class = 'col-xs-8']").get())
        if author =="Đang cập nhật":
            author = ""
        categoryName = list(map(remove_tags,response.xpath("//li[@class = 'kind row']/p[@class = 'col-xs-8']/a").getall()))
        content = remove_tags(response.xpath("//div[@class = 'detail-content']/p").get()) 
        url = response.request.url
        list_chapter = response.xpath("//div[@class = 'col-xs-5 chapter']/a/@href").getall() 
        status = remove_tags(response.xpath("//li[@class = 'author row']/p[@class = 'col-xs-8']").get()) 
        yield Comic(author,last_modified,last_update,url,intro_images,comicName,status,content,list_chapter).__dict__