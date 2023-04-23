import json
import os
import re
from pathlib import Path

from fair_business.objects_storage import fields_xpaths_regexps
from scrapy import Spider
from scrapy.http import Request

source_dir = Path(__file__).parents[4]
cctld_result_file = os.path.join(source_dir, "data/cctld.jl")


class FairBusinessSpider(Spider):

    name = "fair_business"
    base_url = "https://zachestnyibiznes.ru/search?query="

    def start_requests(self):

        with open(cctld_result_file) as f:

            for domain_dict in f.readlines():
                domain_dict = json.loads(domain_dict)

                if domain_dict.get("inn"):
                    yield Request(
                        url=self.base_url + domain_dict["inn"],
                        callback=self.parse,
                        cb_kwargs={"domain_dict": domain_dict},
                    )

                else:
                    yield Request(
                        url="https://egrul.itsoft.ru/",
                        callback=self.save_rows_without_inn,
                        cb_kwargs={"domain_dict": domain_dict}
                    )

    @staticmethod
    def save_rows_without_inn(response, **kwargs):

        yield kwargs["domain_dict"]

    def parse(self, fb_search_response, **kwargs):

        domain_dict = kwargs["domain_dict"]

        regexp = r'<a href=\"(\S+' + re.escape(domain_dict['inn']) + r'\S*)\"'
        raw_links = re.findall(regexp, fb_search_response.text)

        if raw_links:
            link = raw_links[0]
            yield Request(
                url="https://zachestnyibiznes.ru" + link,
                callback=self.get_juridical_info,
                cb_kwargs={
                    "domain_dict": domain_dict
                }
            )

    @staticmethod
    def find_field(x_path, regexp, fb_company_info_response):

        raw_search = None
        try:
            raw_search = re.findall(
                regexp,
                fb_company_info_response.xpath(x_path).get()
            )
        except TypeError:
            pass

        return raw_search[0] if raw_search else None

    def get_juridical_info(self, fb_company_info_response, **kwargs):

        domain_dict = kwargs["domain_dict"]

        for field, x_path, regexp in fields_xpaths_regexps:

            possible_field = self.find_field(x_path, regexp, fb_company_info_response)

            if possible_field:
                domain_dict[field] = possible_field

        raw_headcount = re.findall(r"class=\"c-black zchbLogoTitle\">\n(\d+)", fb_company_info_response.text)

        if raw_headcount:
            domain_dict["headcount"] = raw_headcount[0]

        yield domain_dict
