import scrapy
import logging
from copy import deepcopy
from pmabcSpider.items import PmabcspiderItem

logging = logging.getLogger(__name__)

class PmabcSpider(scrapy.Spider):
    name = 'pmabc'
    allowed_domains = ['pmabc.com']
    start_urls = ['https://www.pmabc.com/']

    def parse(self, response):
        # 1.获取分类
        li_cate = response.xpath("//nav[@class='navbar-left primary-menu']/ul/li")
        for li in li_cate:
            item = {}
            item["cate_href"] = li.xpath("./a/@href").extract_first()
            item["cate_name"] = li.xpath("./a").extract_first()
            yield scrapy.Request(
                item["cate_href"],
                callback=self.parse_list,
                meta={"item": deepcopy(item)}
            )

    def parse_list(self, response):
        # 2.解析每个分类下的列表
        item = deepcopy(response.meta["item"])
        li_list = response.xpath("//div[@class='sec-panel-body']/ul[1]/li")
        for li in li_list:
            item["info_href"] = ''.join(li.xpath("./div[@class='item-content']/h2/a/@href").extract_first())
            item["info_title"] = (''.join(li.xpath("./div[@class='item-content']/h2/a/text()").extract_first())).strip()
            item["info_publish_time"] = ''.join(
                li.xpath("./div[@class='item-content']/div[@class='item-meta']/span/text()").extract_first())
            yield scrapy.Request(
                item["info_href"],
                callback=self.parse_detail,
                meta={"item": deepcopy(item)}
            )
        # 翻页
        next_url = response.xpath("//a[@class='next']/@href").extract_first()
        if next_url is not None:
            yield scrapy.Request(
                next_url,
                callback=self.parse_list,
                meta={"item":response.meta["item"]}
            )

    # 3.详情页处理
    def parse_detail(self, response):
        item = response.meta["item"]
        item["info_content"] = ''.join(response.xpath("//div[@class='entry-content']//p/text()").extract())
        item["info_img"] = ','.join(response.xpath("//div[@class='entry-content']//img/@src").extract())
        print(item)
        print("-" * 100)
        yield item
