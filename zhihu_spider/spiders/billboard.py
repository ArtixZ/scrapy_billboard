# -*- coding: utf-8 -*-
import scrapy
import json

class BillboardSpider(scrapy.Spider):
    name = 'billboard'
    allowed_domains = ['https://zhihu.com/billboard', 'zhihu.com']
    start_urls = ['http://zhihu.com/billboard/']

    def parse(self, response):
        
        initialData = response.xpath('//script[@id="js-initialData"]/text()').extract_first()
        # parsedData = json.dumps(json.loads(initialData), ensure_ascii=False)
        parsedData = json.loads(initialData)

        # hotList = response.xpath('//a[@class="HotList-item"]')
        # for hotItem in hotList:
        #     rank = hotItem.css('.HotList-itemIndexHot').xpath('text()').extract_first()
        #     title = hotItem.css('.HotList-itemTitle').xpath('text()').extract_first()
        #     excerpt = hotItem.css('.HotList-itemExcerpt').xpath('text()').extract_first()
        #     thumbnail = hotItem.css('.HotList-itemImgContainer img').xpath('@src').extract_first()


        #     yield {
        #         'rank': rank.encode('utf-8') if rank else None,
        #         'title': title.encode('utf-8') if title else None,
        #         'excerpt': excerpt.encode('utf-8') if excerpt else None,
        #         'thumbnail': thumbnail,
        #         # 'ReadAmount': readAmount,
        #     }

        hotList = parsedData["initialState"]["topstory"]["hotList"]
        for idx, hotItem in enumerate(hotList):
            target = hotItem["target"]
            rank = idx + 1
            title = target["titleArea"]["text"]
            excerpt = target["excerptArea"]["text"]
            thumbnail = target["imageArea"]["url"]
            url = target["link"]["url"]

            yield scrapy.Request(url, meta={'item': {
                'rank': rank,
                'title': title,
                'excerpt': excerpt,
                'thumbnail': thumbnail,
                'url': url,
            }}, callback=self.parse_second)
            
        
    def parse_second(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        item = response.meta['item'] 
        item["content"] = response.body.decode("utf-8")
        yield item
    