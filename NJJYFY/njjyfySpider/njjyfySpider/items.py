# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NjjyfyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    href = scrapy.Field()
    title = scrapy.Field()
    publish_time = scrapy.Field()
    content = scrapy.Field()
    img = scrapy.Field()
