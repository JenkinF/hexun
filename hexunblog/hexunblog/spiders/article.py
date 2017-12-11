# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from hexunblog.util.headers_util import HeadersUtil
from hexunblog.util.spider_properties import SpiderProperty
from hexunblog.service.article_service import ArticleService
from hexunblog.items import HexunblogItem


class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['hexun.com']

    # start_urls = ['http://hexun.com/']

    def start_requests(self):
        return [Request(url=SpiderProperty.blog_index_url, headers=HeadersUtil.get_default_headers(),
                        callback=self.get_author_urls)]

    '''
    1.爬取排行榜上的用户个人空间地址
    '''

    def get_author_urls(self, response):
        # 排行榜上的用户
        author_urls = response.xpath("//div[@id='zjj_two_1']/ul/li/a/@href").extract()
        if author_urls and len(author_urls) > 0:
            for url in author_urls:
                yield Request(url=url, headers=HeadersUtil.get_default_headers(), callback=self.get_blog_urls)
        else:
            print("未获取到版块")

    '''
    2.获得当前用户所有博文url
    '''

    def get_blog_urls(self, response):
        # 先获取下一页地址
        next_url = response.xpath(u"//div[@class='PageSkip_1']/a[@title='下一页']/@href").extract()
        # 获得所有博文的url
        blog_urls = response.xpath("//div[@class='Article']/div/span/a/@href").extract()
        if blog_urls and len(blog_urls) > 0:
            for url in blog_urls:
                yield Request(url=url, headers=HeadersUtil.get_default_headers(), callback=self.get_blog_info,
                              meta={"url": url})
        else:
            print("未获取到博文")
        # 判断是否有下一页，如果有继续爬
        if next_url and len(next_url) > 0:
            if next_url[0][-12:] != "default.html":
                url = next_url[0] + "default.html"
            else:
                url = next_url[0]
            yield Request(url=url, headers=HeadersUtil.get_default_headers(), callback=self.get_blog_urls)

    '''
    3.获取指定博文的信息
    '''

    def get_blog_info(self, response):
        # 获取博文名称
        article_name = response.xpath("//span[@class='ArticleTitleText']/a/text()").extract()
        # 获得博文的点击量和评论数
        article_click_count, article_comment_count = ArticleService.get_count(response)

        if article_name and article_click_count and article_comment_count and len(article_name) * len(
                article_comment_count) * len(article_click_count) > 0:
            item = HexunblogItem()
            item["article_name"] = article_name[0]
            item["article_click_count"] = article_click_count[0]
            item["article_comment_count"] = article_comment_count[0]
            yield item
        else:
            print("未获取到博文信息")
