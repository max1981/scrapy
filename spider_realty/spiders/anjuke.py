# -*- coding: utf-8 -*-
import scrapy,re
from spider_realty.utils import common
from scrapy.loader import ItemLoader
from spider_realty.items import SpiderRealtyItem
# from scrapy.selector import Selector
from scrapy.spider import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from selenium import webdriver


class AnjukeSpider(CrawlSpider):
    name = "anjuke"
    allowed_domains = ["guangzhou.anjuke.com"]
    handle_httpstatus_list = [404]
    # start_urls = ['https://guangzhou.anjuke.com/']
    start_urls = ['https://guangzhou.anjuke.com/sale/p7']
    rules = [Rule(LinkExtractor(allow=('.*\/prop\/view.*'),),callback='loadTheItem',follow=True,),
             Rule(LinkExtractor(allow=('.*guangzhou.anjuke.com\/sale.*',),),)]

    # 收集404页面统计及url
    def __init__(self):
        self.browser = webdriver.Chrome()
        super(AnjukeSpider,self).__init__()
        dispatcher.connect(self.close_spider,signals.spider_closed)
        self.fail_urls=[]

    def close_spider(self,spider):
        print spider.name + "spider is close"
        self.browser.close()




    # def parse(self, response):
    #     each_page_link = response.xpath('//*[@id="houselist-mod-new"]/li')
    #     for link in each_page_link:
    #         href = link.xpath('div[2]/div[1]/a/@href').extract_first()
    #         yield scrapy.Request(href,callback=self.loadTheItem)
    #     isNext = response.xpath('//*[@id="content"]/div[4]/div[7]/a[9]/text()').extract_first().split(' ')
    #     if isNext[0] == u'下一页':
    #         yield scrapy.Request(response.xpath('//*[@id="content"]/div[4]/div[7]/a[9]/@href').extract_first(),callback=self.parse)



    def loadTheItem(self,response):
        if response.status == 200:
            self.fail_urls.append(response.url)
            self.crawler.stats.inc_value("failed_url")
        item = SpiderRealtyItem()
        item_load = ItemLoader(item=item,response=response)
        # # title = response.xpath('//*[@id="content"]/div[2]/h3').extract_first()
        # title = response.css('.long-title::text').extract_first()
        # # price =  response.xpath('//*[@id="content"]/div[3]/div[1]/div[1]/span[1]/em').extract_first()
        # price = response.css('.light.info-tag em::text').extract_first()
        # # area = response.xpath('//*[@id="content"]/div[3]/div[1]/div[1]/span[3]/em').extract_first()
        # area = response.css('.second-col.detail-col dl:nth-child(2) dd::text').extract_first()
        # # avg_price = response.xpath('//*[@id="content"]/div[3]/div[1]/div[3]/div/div/div[1]/div[3]/dl[2]/dd').extract_first()
        # avg_price = response.css('.third-col.detail-col dl:nth-child(2) dd::text').extract_first()
        # # decoration = response.xpath('//*[@id="content"]/div[3]/div[1]/div[3]/div/div/div[1]/div[3]/dl[1]/dd').extract_first()
        # decoration = response.css('.third-col.detail-col dl:nth-child(1) dd::text').extract_first()
        # # build_time = response.xpath('//*[@id="content"]/div[3]/div[1]/div[3]/div/div/div[1]/div[1]/dl[3]/dd').extract_first()
        # build_time = response.css('.first-col.detail-col dl:nth-child(3) dd::text').extract_first()
        # # orientation = response.xpath('//*[@id="content"]/div[3]/div[1]/div[3]/div/div/div[1]/div[2]/dl[3]/dd').extract_first()
        # orientation = response.css('.second-col.detail-col dl:nth-child(3) dd::text').extract_first()
        # # build_type = response.xpath('//*[@id="content"]/div[3]/div[1]/div[3]/div/div/div[1]/div[1]/dl[4]/dd').extract_first()
        # build_type = response.css('.first-col.detail-col dl:nth-child(4) dd::text').extract_first()
        lat = re.findall('lat : "(.*)"',response.body)[0]
        lng = re.findall('lng : "(.*)"',response.body)[0]
        locationX = lat
        locationY = lng
        # addr = response.xpath('//*[@id="content"]/div[3]/div[1]/div[3]/div/div/div[1]/div[1]/dl[2]/dd').extract_first()
        addr_1 = response.css('.loc-text a::text').extract()
        addr_1 = '-'.join(addr_1)
        addr_2 = response.css('.loc-text::text').extract()[-1]
        addr_2 = addr_2.split(' ')[-1]
        addr = addr_1+"_"+addr_2

        link = response.url
        link_md5 = common.get_md5(link)
        # item["title"] = title
        # item["price"] = price
        # item["area"] = area
        # item["avg_price"] = avg_price
        # item["decoration"] = decoration
        # item["build_time"] = build_time
        # item["orientation"] = orientation
        # item["build_type"] = build_type
        # item["locationX"] = locationX
        # item["locationY"] = locationY
        # item["addr"] = addr
        # item["link"] = link
        # item["link_md5"] = link_md5

        item_load.add_css('title', '.long-title::text')
        item_load.add_css('price', '.light.info-tag em::text')
        item_load.add_css('area', '.second-col.detail-col dl:nth-child(2) dd::text')
        item_load.add_css('avg_price', '.third-col.detail-col dl:nth-child(2) dd::text')
        item_load.add_css('decoration', '.third-col.detail-col dl:nth-child(1) dd::text')
        item_load.add_css('build_time', '.first-col.detail-col dl:nth-child(3) dd::text')
        item_load.add_css('orientation', '.second-col.detail-col dl:nth-child(3) dd::text')
        item_load.add_css('build_type', '.first-col.detail-col dl:nth-child(4) dd::text')
        item_load.add_value('locationX', locationX)
        item_load.add_value('locationY', locationY)
        item_load.add_value('addr', addr)
        item_load.add_value('link', link)
        item_load.add_value('link_md5', link_md5)
        item_load.load_item()

        yield item_load.load_item()

