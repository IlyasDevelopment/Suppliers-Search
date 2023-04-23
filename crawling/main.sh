#!/bin/bash

rm data/juridical_info.jl

cd /opt/app/spiders/search_engines/search_engines/spiders && scrapy runspider search.py
echo SEARCH SCRAPING ENDED: 1 out of 4

cd /opt/app/spiders/suppliers/suppliers/spiders && scrapy runspider main_page.py
echo SUPPLIERS SCRAPING ENDED: 2 out of 4

cd /opt/app/spiders/cctld/cctld/spiders && scrapy runspider whois.py
echo WHOIS SCRAPING ENDED: 3 out of 4

cd /opt/app/spiders/fair_business/fair_business/spiders && scrapy runspider juridical_info.py
echo FAIR_BUSINESS SCRAPING ENDED: 4 out of 4

cd /opt/app && python upload_data.py
echo THE COLLECTED DATA HAS BEEN UPLOADED TO THE DATABASE SUCCESSFULLY
