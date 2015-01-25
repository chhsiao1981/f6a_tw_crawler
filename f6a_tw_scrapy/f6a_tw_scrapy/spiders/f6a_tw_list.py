# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from f6a_tw_scrapy.items import F6ATwScrapyItem
import logging
from lxml import html


class F6aTwListSpider(scrapy.Spider):
    name = "f6a_tw_list"
    allowed_domains = ["data.fda.gov.tw"]

    def __init__(self, no=1, *args, **kwargs):
        self.no = no
        self.start_urls = [
            'http://data.fda.gov.tw/frontsite/data/DataAction.do?method=doDetail&infoId=' + str(no)
        ]
        super(F6aTwListSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        logging.warning('response.url: %s', response.url)
        sel = Selector(response)

        name_node = sel.xpath('//div[@class="main"]/div[@class="datascont_mobile"]/h2/text()')
        name = name_node.extract()
        name = '' if not name else name[0]

        desc_node = sel.xpath('//div[@class="main"]/div[@class="datascont_mobile"]/div[@class="datascont_mobile_desc"]/text()')
        desc = desc_node.extract()
        desc = '' if not desc else desc[0]

        type_node = sel.xpath('//div[@class="main"]/div[@class="datascont_mobile"]/div[@class="data_class"]/span/text()')
        the_type = type_node.extract()
        the_type = '' if not the_type else the_type[0]

        provider_node = sel.xpath('//div[@class="main"]/div[@class="datascont_mobile"]/div[@class="data_prov"]/span/text()')
        provider = provider_node.extract()
        provider = '' if not provider else provider[0]

        fields_node = sel.xpath('//table[@class="table_Info"]/tr|//table[@class="table_Info"]/tbody')
        fields_node = fields_node.extract()

        columns = []
        update_date = ''
        try:
            for each_field in fields_node:
                logging.warning('each_field: %s', each_field)
                each_sel = html.fromstring(each_field)
                node_key = each_sel.xpath('//th/text()')
                node_key = '' if not node_key else node_key[0].strip()
                node_val = each_sel.xpath('//td/text()')
                node_val = '' if not node_val else node_val[0].strip()
                logging.warning('node_key: %s node_val: %s', node_key, node_val)

                if node_key == u'主要欄位說明':
                    columns = node_val.split(u'、')
                elif node_key == u'最後更新日期':
                    update_date = node_val
        except Exception as e:
            logging.error('some error happened: e: %s', e)

        item = F6ATwScrapyItem()
        item['name'] = name
        item['the_id'] = self.no
        item['the_url'] = response.url
        item['desc'] = desc
        item['the_type'] = the_type
        item['provider'] = provider
        item['update_date'] = update_date
        item['columns'] = columns

        logging.warning('item: %s', item)

        return item
