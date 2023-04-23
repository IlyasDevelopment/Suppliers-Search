# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class DomainItem(Item):
    domain = Field()
    inn = Field()
    title = Field()
    products = Field()
    products_num = Field()
    phone = Field()
    email = Field()
