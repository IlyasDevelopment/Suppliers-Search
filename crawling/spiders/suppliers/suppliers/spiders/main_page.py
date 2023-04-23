import json
import os
import re
from collections import Counter
from pathlib import Path

import scrapy

source_dir = Path(__file__).parents[4]
search_result_file = os.path.join(source_dir, "data/search.jl")


class SuppliersSpider(scrapy.Spider):

    name = "suppliers"

    def start_requests(self):

        with open(search_result_file) as f:

            for domain_dict in f.readlines():
                domain_dict = json.loads(domain_dict)

                url = f"https://www.{domain_dict['domain']}/"

                yield scrapy.Request(url=url, callback=self.get_title_and_contacts, cb_kwargs={"domain_dict": domain_dict})

    @staticmethod
    def get_title_and_contacts(index_page_response, **kwargs):

        domain_dict = kwargs["domain_dict"]

        domain_dict["title"] = index_page_response.xpath("//title/text()").get()

        raw_emails = re.findall(r"[\w\.-]+@[\w\.-]+(?:\.[\w]+)+", index_page_response.text)
        if raw_emails:
            emails = list(filter(lambda x: x.split('.')[1].isalpha(), raw_emails))
            if emails:
                domain_dict["email"] = Counter(emails).most_common(1)[0][0]

        raw_phones_1 = re.findall(
            r"[(\+7|7|8)][\s\-]?\(?[0-9]{3}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}\D",
            index_page_response.text
        )

        raw_phones_2 = re.findall(
            r"[(\+7|7|8)][\s\-]?\(?[0-9]{4}\)?[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}\D",
            index_page_response.text
        )

        raw_phones = raw_phones_1 + raw_phones_2
        if raw_phones:
            phone = Counter(["".join(filter(str.isdigit, phone)) for phone in raw_phones]).most_common(1)[0][0]
            domain_dict["phone"] = "+" + phone if phone.startswith("7") else phone

        yield domain_dict
