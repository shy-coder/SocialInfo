import scrapy
import logging
from copy import deepcopy
from time import sleep
from NJDaily.items import NjdailyItem

logging = logging.getLogger(__name__)


class NjdSpider(scrapy.Spider):
    name = 'NJD'
    allowed_domains = ['njdaily.cn']
    start_urls = ['http://www.njdaily.cn']

    def parse(self, response):
        # 1.获取总分类
        li_cate = response.xpath("//div[@class='header-nav clearfix']/li")
        for li in li_cate:
            item = {}
            item["cate_name"] = ''.join(li.xpath("./span/a/text()").extract_first())  # 分类名
            item["cate_href"] = ''.join(li.xpath("./span/a/@href").extract_first())  # 分类连接
            yield scrapy.Request(
                item["cate_href"],
                callback=self.deal_cate,
                meta={"item": item}
            )

    # 2.解析每个分类下的数据（获取总数，总页数，拆分url）
    def deal_cate(self, response):
        item = response.meta["item"]
        # 获取当前分类下信息的总数量
        info_total = 0
        temp_info_total = response.xpath("//div[@class='pagination']/@total").extract_first()
        if temp_info_total is not None:
            info_total = int(''.join(temp_info_total))
        item["cate_info_total"] = info_total

        # 通过总数计算出总页数
        page_total = 0
        if info_total % 10 > 0 and info_total is not None:
            page_total = int(info_total / 10 + 1)
            item["cate_page_total"] = page_total
        else:
            page_total = int(info_total / 10)
            item["cate_page_total"] = page_total

        if info_total > 0:
            url = item["cate_href"]
            url_list = url.split('1')
            item["cate_href_pre"] = url_list[0]
            print("！！！！！！！！！！我是总分类：", item, "！！！！！！！！！！")
            yield scrapy.Request(
                item["cate_href"],
                callback=self.parse_list,
                meta={"item": deepcopy(item),
                      "page_index": 1,
                      },
                dont_filter=True
            )

    # 3.循环遍历大分类下的分页列表
    def parse_list(self, response):
        item = deepcopy(response.meta["item"])
        page_index = response.meta["page_index"]
        print("获取到的page_index", page_index)

        # 根据总页数进行遍历页面
        div_list = response.xpath("//div[@class='container-left']/div[@class='list-item clearfix']")
        for div_item in div_list:
            item["info_title"] = ''.join(div_item.xpath(".//a/text()").extract_first())
            item["info_href"] = ''.join(div_item.xpath(".//a/@href").extract_first())
            print("**********下一步交给详情页处理了：", item,"**********")
            yield scrapy.Request(
                item["info_href"],
                callback=self.parse_detail,
                meta={"item": deepcopy(item)}
            )

        # 翻页
        page_index = page_index + 1
        next_url = item["cate_href_pre"] + str(page_index) + ".html"
        print("拼接的url!!!!!!!!!!!", next_url)
        if page_index <= item["cate_page_total"]:
            yield scrapy.Request(
                next_url,
                callback=self.parse_list,
                meta={"item": response.meta["item"],
                      "page_index": page_index
                      }
            )

    # 4.详情页处理
    def parse_detail(self, response):
        item = response.meta["item"]
        item["info_publish_time"] = ''.join(response.xpath("//div[@class='news-title']/span[1]/text()").extract_first())
        item["info_content"] = ''.join(response.xpath("//div[@class='news-ctx']/p//text()").extract())
        item["info_img"] = ''.join(response.xpath("//div[@class='news-ctx']//img/@src").extract())
        print("处理好的：", item)
        print("-" * 100)
        yield item
