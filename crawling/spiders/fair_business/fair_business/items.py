# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class FairBusinessItem(Item):
    domain = Field()
    products_num = Field()
    products = Field()
    title = Field()
    email = Field()
    phone = Field()
    inn = Field()
    psrn = Field()
    fair_business_rating = Field()
    fair_business_rating_comment = Field()
    registration_date = Field()
    main_activity = Field()
    authorized_capital = Field()
    profit = Field()
    name = Field()
    headcount = Field()
