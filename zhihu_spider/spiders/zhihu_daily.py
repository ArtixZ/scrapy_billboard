# -*- coding: utf-8 -*-
import scrapy
import json

class ZhihuDailySpider(scrapy.Spider):
    name = 'zhihu_daily'
    custom_settings = {
        'ITEM_PIPELINES': {
            'zhihu_spider.pipelines.MongoDBDaily': 800
        }
    }
    # allowed_domains = ['https://www.zhihu.com/explore']
    # start_urls = ['http://https://www.zhihu.com/explore/']
    top_activity = 'https://www.zhihu.com/api/v4/topics/{0}/feeds/top_activity?include=data%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Danswer)%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Danswer)%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Darticle)%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Dpeople)%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Danswer)%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F(target.type%3Danswer)%5D.target.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Darticle)%5D.target.content%2Cauthor.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dquestion)%5D.target.comment_count&offset={1}&limit={2}'

    def start_requests(self):
        topic_id = 19556664
        yield scrapy.Request(
            url=self.top_activity.format(topic_id, 0, 10),
            method='GET',
            meta={'topic_id': topic_id, 'count': 0, 'url': self.top_activity.format(topic_id, 0, 10)},
            # headers=self.headers,
            dont_filter=True,
            callback=self.parse_top_activity,)

    def parse_top_activity(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        resJson = json.loads(response.body)
        data = resJson['data']

        for item in data:
            target = item['target']
            yield {
                'id': target['id'],
                'type': target['type'],
                'comment_count': target['comment_count'],
                'created_time': target['created_time'],
                'author': target['author'],
                'content': target['content'],
                'excerpt': target['excerpt'],
                'url': target['url'],
                'voteup_count': target['voteup_count'],
                'question': target['question'],
                'updated_time': target['updated_time'],
            }
    
    def parse(self, response):
        pass
