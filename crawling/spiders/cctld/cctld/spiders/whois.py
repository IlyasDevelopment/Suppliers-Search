import json
import os
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urljoin

from cctld.items import DomainItem
from cctld.loaders import DomainLoader
from scrapy import Spider
from scrapy.http import Request

source_dir = Path(__file__).parents[4]
contacts_result_file = os.path.join(source_dir, "data/contacts.jl")


class WhoisSpider(Spider):

    name = "whois"
    base_url = "https://cctld.ru/tci-ripn-rdap/domain/"

    handle_httpstatus_list = [404]

    def start_requests(self):

        with open(contacts_result_file) as f:

            for domain_dict in f.readlines():
                domain_dict = json.loads(domain_dict)

                yield Request(
                    url=urljoin(self.base_url, domain_dict["domain"]),
                    callback=self.parse,
                    cb_kwargs={"domain_dict": domain_dict},
                )

    def parse(self, whois_response, **kwargs):

        domain_dict = kwargs["domain_dict"]

        loader = DomainLoader(DomainItem())

        for field in domain_dict:
            loader.add_value(field, domain_dict[field])

        entities = whois_response.json().get("entities")

        inn = None
        if entities:
            inn = entities[1].get("ripn_tax_payer_number")

        if inn:
            domain_dict["inn"] = inn
            yield domain_dict
        else:
            yield Request(
                url="https://yandex.ru/search/?text={}+inn+company".format(domain_dict["domain"]),
                callback=self.parse_yandex,
                cb_kwargs={
                    "domain_dict": domain_dict
                },
            )

    def parse_yandex(self, yandex_search_response, **kwargs):

        domain_dict = kwargs["domain_dict"]

        raw_inns = re.findall(r"<b>ИНН</b>.? (\d{10})[)<,.\s]+", yandex_search_response.text)

        if raw_inns:
            inn = Counter(raw_inns).most_common(1)[0][0]

            if inn:
                domain_dict["inn"] = inn

        yield domain_dict
