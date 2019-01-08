# -*- coding: utf-8 -*-
import scrapy
import json
import os
import logging
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup as bs

with open(os.path.join(os.path.dirname(__file__), "../config.json")) as topics:
    topics = json.load(topics)["zhihu_topic"]

class ZhihuDailySpider(scrapy.Spider):
    name = 'zhihu_daily'
    custom_settings = {
        'ITEM_PIPELINES': {
            'zhihu_spider.pipelines.MongoDBDaily': 800
        }
    }
    allowed_domains = ['https://www.zhihu.com']
    # start_urls = ['http://https://www.zhihu.com/explore/']
    top_activity = 'https://www.zhihu.com/api/v4/topics/{0}/feeds/top_activity?include=data%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Danswer)%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Danswer)%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Darticle)%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Dpeople)%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Danswer)%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F(target.type%3Danswer)%5D.target.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Darticle)%5D.target.content%2Cauthor.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dquestion)%5D.target.comment_count&offset={1}&limit={2}'
    answer_url = "https://www.zhihu.com/question/{0}/answer/{1}"
    
    def start_requests(self):
        for topic in topics:
            # import pdb; pdb.set_trace()
            topic_id = topic["id"]
            yield scrapy.Request(
                url=self.top_activity.format(topic_id, 0, 10),
                method='GET',
                meta={'topic_id': topic_id, 'count': 0, 'url': self.top_activity.format(topic_id, 0, 10)},
                # headers=self.headers,
                dont_filter=True,
                callback=self.parse_top_activity,)

    def parse_top_activity(self, response):
        
        meta = response.meta
        resJson = json.loads(response.body)
        data = resJson['data']


        for item in data:
            target = item['target']

            # from scrapy.shell import inspect_response
            # inspect_response(response, self)
            if target["type"] == "article":
                answer_page_url = target["url"]

                yield SplashRequest(
                    url=answer_page_url,
                    method='GET',
                    dont_filter=True,
                    callback=self.parse_tag,
                    meta={
                        'id': target['id'],
                        'type': target['type'],
                        'comment_count': target['comment_count'],
                        # 'created_time': target['created_time'],
                        'author': target['author'],
                        'content': target['content'],
                        'excerpt': target['excerpt'],
                        'url': answer_page_url,
                        'voteup_count': target['voteup_count'],
                        # 'question': target['question'],
                        # 'updated_time': target['updated_time'],
                        'topic_id': meta['topic_id'],
                    }
                )
            elif target["type"] == "answer":
                answer_page_url = self.answer_url.format(target["question"]["url"].split("/")[-1] ,target["url"].split('/')[-1])

                yield SplashRequest(
                    url=answer_page_url,
                    method='GET',
                    dont_filter=True,
                    callback=self.parse_tag,
                    meta={
                        'id': target['id'],
                        'type': target['type'],
                        'comment_count': target['comment_count'],
                        'created_time': target['created_time'],
                        'author': target['author'],
                        'content': target['content'],
                        'excerpt': target['excerpt'],
                        'url': answer_page_url,
                        'voteup_count': target['voteup_count'],
                        'question': target['question'],
                        'updated_time': target['updated_time'],
                        'topic_id': meta['topic_id'],
                    }
                )
    
    def parse_tag(self, response):

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        soup = bs(response.body, 'lxml')
        # 知乎专栏的tag 和 thumbnail:
        if response.meta["type"] == "article":
            raw_topics = soup.select_one("div.TopicList").select("div.Topic")
            topics = [x.text for x in raw_topics]
            try:
                if soup.select_one("img.TitleImage"): 
                    thumbnail = soup.select_one("img.TitleImage")["src"]
                else:
                    thumbnail = soup.select_one(".Post-RichText").select_one("img")["data-original"]
            except:
                thumbnail = None

        # 知乎问答的tag 和 thumbnail：
        elif response.meta["type"] == "answer":
            raw_topics = soup.findAll("div", {"class": "Tag QuestionTopic"})
            topics = [x.text for x in raw_topics]
            try:
                thumbnail = soup.select_one("div.RichContent").select_one("img")["src"]
            except:
                thumbnail = None

        payload = response.meta

        payload["tags"] = topics
        payload["thumbnail"] = thumbnail
        yield payload
        # print("!!!!!!!!!!!!" , response.body)

        # topics = response.css('.QuestionHeader-topics')

        # print("!!!!!", response.body.decode("utf-8"))
        
    

    def parse(self, response):
        pass
