# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random,requests,time
from selenium import webdriver
from scrapy.http import HtmlResponse


class SpiderRealtySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class proxyMiddleware(object):
    def __init__(self):
        self.ips = []
        with open("d:\\realIP.txt",'r') as f:
            tmp = f.readlines()[0]
            self.ips = tmp.split(',')
            self.ips.remove('')
    # def iswork(self,ip):
    #     try:
    #         ip = ip.lower()
    #         headers = {'content-type': 'application/json',
    #                    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    #         ip_type = ip.split('://')[0]
    #         print "*"*20
    #         res = requests.get('https://guangzhou.anjuke.com/', proxies={ip_type: ip},headers=headers)
    #         if not res.status_code == 200:
    #             print 'connect failed' + ip
    #             return False
    #     except:
    #         print 'connect failed'+ip
    #         return False
    #     else:
    #         # print 'success'
    #         return True

    def process_request(self,request,spider):
        rip = random.choice(self.ips)
        print rip
        request.meta['proxy']=rip

class JSPageMiddleware(object):

    def process_request(self,request,spider):
        if  spider.name== "anjuke":
            spider.browser = webdriver.Chrome()
            spider.browser.get(request.url)
            time.sleep(3)
            print "Get"+request.url
            return HtmlResponse(url = spider.browser.current_url,body=spider.browser.page_source,encoding="utf-8",request=request)


