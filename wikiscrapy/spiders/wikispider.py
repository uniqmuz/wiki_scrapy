# -*- coding: utf-8 -*-
import logging
import scrapy
from wikiscrapy.spiders import wiki_parser
from scrapy.conf import settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class WikispiderSpider(scrapy.Spider):
    name = 'wikispider'
    allowed_domains = ['ko.wikipedia.org']
    url = ''
    keyworld = ''

    def __init__(self, *args, **kwargs):
        #from async_spider_runner.py
        self.keyword = kwargs.pop('keyword', str)
        self.url = 'https://ko.wikipedia.org/w/index.php?search=' + self.keyword + '&title=특수%3A검색&profile=default&fulltext=1'
        super(WikispiderSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        urls = response.xpath("//div[@class='mw-search-result-heading']/a/@href").extract()
        #header = response.xpath("//div[@class='mw-search-result-heading']/a/@title").extract()
        logging.info("urls : " + str(urls))
        for url in urls:
            #logging.info("go_content - url" + url)
            yield scrapy.Request(url="http://ko.wikipedia.org/" + url, callback=self.content_parse)

        next_link = response.xpath("//a[@class='mw-nextlink']/@href").extract_first()
        if next_link is not None:
            logging.info("========next page=========")
            next_page = 'http://ko.wikipedia.org' + response.xpath("//a[@class='mw-nextlink']/@href").extract_first()
            yield scrapy.Request(url=next_page, callback=self.parse)

    def content_parse(self, response):
        title = response.xpath('//*[@id="firstHeading"]/text()').extract()
        content = response.xpath('//*[@id="mw-content-text"]/div/p').extract()
        #logging.info("title : " + str(title))
        logging.info("content : " + str(content))
        #filename = self.keyword + '.result'
        #with open(filename, 'ab') as f:
        #    f.write(str(content).encode('euc-kr'))