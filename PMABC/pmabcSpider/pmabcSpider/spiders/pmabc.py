import scrapy
import logging
from pmabcSpider.items import PmabcspiderItem

logging = logging.getLogger(__name__)

class PmabcSpider(scrapy.Spider):
    name = 'pmabc'
    allowed_domains = ['pmabc.com']
    start_urls = ['https://www.pmabc.com/category/pmnews']

    def parse(self, response):
        li_list = response.xpath("//div[@class='sec-panel-body']/ul[1]/li")
        next_href = response.xpath("//div[@class='sec-panel-body']/ul[2]/li[@class='next']/a/@href")
        for li in li_list:
            item = PmabcspiderItem()
            item["href"] = ''.join(li.xpath("./div[@class='item-content']/h2/a/@href").extract_first())
            item["title"] = (''.join(li.xpath("./div[@class='item-content']/h2/a/text()").extract_first())).strip()
            item["publish_time"] = ''.join(li.xpath("./div[@class='item-content']/div[@class='item-meta']/span/text()").extract_first())
            yield scrapy.Request(
                item["href"],
                callback=self.parse_detail,
                meta={"item":item}
            )
        #翻页
        next_url = response.xpath("//a[@class='next']/@href").extract_first()
        if next_url is not None:
            yield  scrapy.Request(
                next_url,
                callback=self.parse
            )

    #详情页处理
    def parse_detail(self,response):
        item = response.meta["item"]
        item["content"] = ''.join(response.xpath("//div[@class='entry-content']/p/text()").extract())
        item["img"] = ','.join(response.xpath("//div[@class='entry-content']//img/@src").extract())
        print(item)
        print("-"*66)
        yield item