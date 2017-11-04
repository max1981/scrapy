# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy,re
from scrapy.loader.processors import MapCompose,TakeFirst

def get_math(s):
    value = re.findall('\d+\.*\d+', s)[0]
    return value

def set_code_type(s):
    if type(s) == type('str'):
        return s.encode('utf8').replace('\n','').replace('\t','')
    return s


class SpiderRealtyItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(set_code_type),
        output_processor = TakeFirst()
    )
    price = scrapy.Field(
        input_processor = MapCompose(set_code_type,get_math),
        output_processor = TakeFirst()
    )
    area = scrapy.Field(
        input_processor=MapCompose(set_code_type,get_math),
        output_processor = TakeFirst()
    )
    avg_price = scrapy.Field(
        input_processor=MapCompose(set_code_type,get_math),
        output_processor = TakeFirst()
    )
    decoration = scrapy.Field(
        input_processor=MapCompose(set_code_type),
        output_processor = TakeFirst()
    )
    build_time = scrapy.Field(
        input_processor=MapCompose(set_code_type),
        output_processor = TakeFirst()
    )
    orientation = scrapy.Field(
        input_processor=MapCompose(set_code_type),
        output_processor = TakeFirst()
    )
    build_type = scrapy.Field(
        input_processor=MapCompose(set_code_type),
        output_processor = TakeFirst()
    )
    locationX = scrapy.Field(
        input_processor=MapCompose(get_math),
        output_processor = TakeFirst()
    )
    locationY = scrapy.Field(
        input_processor=MapCompose(get_math),
        output_processor = TakeFirst()
    )
    addr = scrapy.Field(
        input_processor=MapCompose(set_code_type),
        output_processor = TakeFirst()
    )
    link = scrapy.Field(
        output_processor = TakeFirst()
    )
    link_md5 = scrapy.Field(
        input_processor=MapCompose(set_code_type),
        output_processor = TakeFirst()
    )

    def insert_sql(self):
        insert_sql = "insert into realtyitem(title, price, area, avg_price,decoration,build_time,orientation,build_type,locationX,locationY,addr,link,link_md5) VALUES ('%s', %s, %s, %s, '%s', '%s', '%s', '%s', %s, %s, '%s', '%s', '%s')"
        sql = insert_sql % (
        self["title"], self["price"], self["area"], self["avg_price"], self["decoration"], self["build_time"], self["orientation"], self["build_type"], self["locationX"], self["locationY"],
        self["addr"], self["link"], self["link_md5"])

        return sql


class ip_proxpItem(scrapy.Item):
    ip_port = scrapy.Field()

