import json
import os
import re
import zipfile
from pathlib import Path

import scrapy
from scrapy import signals
from search_engines.objects_storage import skip_domains

source_dir = Path(__file__).parents[4]
search_result_file = os.path.join(source_dir, "data/search.jl")
desired_goods_file = os.path.join(source_dir, "data/desired_goods.xlsx")


class SearchSpider(scrapy.Spider):

    name = "search"

    found_domains = set()
    domains_data = dict()

    def start_requests(self):

        with zipfile.ZipFile(desired_goods_file) as z:
            for file in z.namelist():
                if "sharedStrings" in file:
                    with z.open(file) as f:
                        for product in re.findall("<t>\* (.+?)</t>", f.read().decode()):

                            request_text = re.sub("ГОСТ\s+\d+", "", product)

                            yandex_url = f"https://yandex.ru/search/?text={request_text}&lr=225"

                            yield scrapy.Request(
                                url=yandex_url,
                                callback=self.parse,
                                cb_kwargs={
                                    "product": product
                                })

    def parse(self, search_engine_response, **kwargs):

        for probable_resource in search_engine_response.xpath("//*[@id=\"search-result\"]/li/div/div[1]/a").getall():

            probable_domains = re.findall("http[s]*://(?:www\.|)(.+?\.com|.+?\.ru)/", probable_resource)

            if probable_domains:
                probable_domains = list(filter(lambda x: len(x) <= 22, probable_domains))
                probable_domains = set(probable_domains) - skip_domains

            if probable_domains:

                domain = min(tuple(probable_domains))

                if domain not in self.found_domains:

                    self.domains_data[domain] = {
                        "domain": domain,
                        "products_num": 1,
                        "products": [kwargs["product"]]
                    }

                    self.found_domains.add(domain)

                elif domain in self.found_domains:

                    if kwargs["product"] not in self.domains_data[domain]["products"]:

                        self.domains_data[domain]["products_num"] += 1
                        self.domains_data[domain]["products"].append(kwargs["product"])

    def spider_closed(self, spider):

        with open(search_result_file, "w") as f:

            for domain_data in self.domains_data.values():
                f.write(json.dumps(domain_data) + "\n")

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):

        spider = super(SearchSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)

        return spider
