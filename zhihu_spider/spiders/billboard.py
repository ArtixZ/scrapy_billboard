# -*- coding: utf-8 -*-
import scrapy


class BillboardSpider(scrapy.Spider):
    name = 'billboard'
    allowed_domains = ['https://zhihu.com/billboard']
    start_urls = ['http://zhihu.com/billboard/']

    def parse(self, response):
        hotList = response.xpath('//a[@class="HotList-item"]')
        for hotItem in hotList:
            [idx, title, readAmount] = hotItem.xpath('.//text()').extract()
            yield {
                'Index': idx,
                'Title': title,
                'ReadAmount': readAmount,
            }