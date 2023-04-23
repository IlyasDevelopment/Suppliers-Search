# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class SuppliersItem(Item):
    domain = Field()
    title = Field()
    avg_place_in_search = Field()
    products_num = Field()
    products = Field()
    email = Field()
    phone = Field()
