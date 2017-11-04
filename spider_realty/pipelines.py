# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

class SpiderRealtyPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1','root','netease', 'realty',charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = item.insert_sql()
        self.cursor.execute(sql)
        self.conn.commit()
    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()

class IPProxyPipleline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1','root','netease', 'realty',charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self,item,spider):
        sql = 'insert into ipproxy values %s'%item
        self.cursor.execute(sql)
        self.conn.commit()

    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()
