# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class F6ATwScrapyItem(Item):
    name = Field()
    the_id = Field()
    the_url = Field()
    desc = Field()
    the_type = Field()
    provider = Field()
    update_date = Field()
    columns = Field()
