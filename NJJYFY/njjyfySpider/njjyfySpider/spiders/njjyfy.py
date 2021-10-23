# -*- codeing = utf-8 -*-
import scrapy
import logging
from njjyfySpider.items import NjjyfyspiderItem

logging = logging.getLogger(__name__)

class NjjyfySpider(scrapy.Spider):
    name = 'njjyfy'
    allowed_domains = ['njjyfy.gov.cn']
    start_urls = ['http://www.njjyfy.gov.cn/njxxweb_publishing/www/jyfyww/xwzx.html']

    # 列表
    def parse(self, response):
        pre_path = "http://www.njjyfy.gov.cn/njxxweb_publishing/www/jyfyww/"
        #分组
        li_list = response.xpath("//ul[@id='result']//li")
        for li in li_list:
            item = NjjyfyspiderItem()
            item["href"] = ''.join(pre_path + li.xpath("./a/@href").extract_first())
            print("获取到的链接————————————："+item["href"])
            item["title"] = ''.join(li.xpath("./a/text()").extract_first())
            item["publish_time"] = ''.join(li.xpath("./span/text()").extract_first())
            yield scrapy.Request(
                item["href"],
                callback=self.parse_detail,
                meta={"item":item}
            )
        print(len(item["href"]))

    # 详情页
    def parse_detail(self,response):
        item = response.meta["item"]
        item["content"] = ''.join(response.xpath("//div[@class='nrwz']//text()").extract())
        item["img"] = ','.join(response.xpath("//div[@class='con']//img/@src").extract())
        print(item)
        yield item

    '''
    start_urls = ['http://www.njjyfy.gov.cn/njxxweb_publishing/www/jyfyww/xwzx_mb_a2021091037302.html']
    def parse(self, response):
        # 提取数据
        item = NjjyfyspiderItem()
        item["title"] = ''.join(response.xpath("//div[2]//div[2]//div[2]//div//div[@class='con_title'][1]//text()").extract())
        item["date"] = ''.join(response.xpath("//div[2]//div[2]//div[2]//div//div[2]//div[1]//text()").extract())
        item["content"] = ''.join(response.xpath("//div[2]//div[2]//div[2]//div//div[@class='nrwz']//p//text()").extract())
        # item = {"title": title, "date": date, "content": content}
        yield item

        next_url = response.xpath("//div[@class='con_pre'][2]//a//@href").extract_first()
        if not next_url is None:
            print("****************下一页***************")
            next_url = "http://www.njjyfy.gov.cn/njxxweb_publishing/www/jyfyww/" + next_url;
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )
    '''
