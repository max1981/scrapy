#coding:utf8
from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "anjuke"])
# execute(["scrapy", "crawl", "ip_proxy"])