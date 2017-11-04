# -*- coding: utf-8 -*-
import scrapy
from spider_realty.items import ip_proxpItem


class IpProxySpider(scrapy.Spider):
    name = "ip_proxy"
    allowed_domains = ["xicidaili.com"]
    start_urls = []
    for i in xrange(1,11):
        s = 'http://www.xicidaili.com/nn/'+str(i)
        start_urls.append(s)

    base_url = 'http://www.xicidaili.com'

    def parse(self, response):
        values = response.css('#ip_list tr')
        # item = ip_proxpItem()
        for value in values:
            ip = value.css('td:nth-child(2)::text').extract_first()
            port = value.css('td:nth-child(3)::text').extract_first()
            ip_type = value.css('td:nth-child(6)::text').extract_first()
            if not ip:
                continue
            with open('d:\\IPProxy.txt','a') as f:
                f.write(ip_type+"://"+ip+":"+port+',')

