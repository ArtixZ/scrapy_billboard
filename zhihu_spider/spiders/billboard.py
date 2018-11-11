# -*- coding: utf-8 -*-
import scrapy


class BillboardSpider(scrapy.Spider):
    name = 'billboard'
    allowed_domains = ['https://zhihu.com/billboard']
    start_urls = ['http://zhihu.com/billboard/']

    def parse(self, response):
        pass
