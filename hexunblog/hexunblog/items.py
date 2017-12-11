# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HexunblogItem(scrapy.Item):

    article_name = scrapy.Field()

    article_click_count = scrapy.Field()

    article_comment_count = scrapy.Field()
