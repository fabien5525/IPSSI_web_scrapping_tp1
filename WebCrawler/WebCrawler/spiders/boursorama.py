import datetime
from typing import Iterable
import scrapy
from scrapy.http import Request
from ..items import BoursoramaItem


class BoursoramaSpider(scrapy.Spider):
    name = "boursorama"
    allowed_domains = ["www.boursorama.com"]

    # get gthe first 2 pages of https://www.boursorama.com/bourse/actions/palmares/france/page-{}?france_filter%5Bmarket%5D=1rPCAC
    start_urls = [ f'https://www.boursorama.com/bourse/actions/palmares/france/page-{i}?france_filter%5Bmarket%5D=1rPCAC' for i in range(1, 3) ]

    def start_requests(self) -> Iterable[Request]:
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)
    
    def parse(self, response):
        items = response.css('div.c-palmares tr.c-table__row')[1:]

        for item in items:
            boursomaraItem = BoursoramaItem()

            boursomaraItem['label'] = item.css('a.c-link::text').get()
            boursomaraItem['last'] = item.css('span.c-instrument.c-instrument--last::text').get()
            boursomaraItem['variation'] = item.css('span.c-instrument.c-instrument--instant-variation::text').get()
            boursomaraItem['opening'] = item.css('span.c-instrument.c-instrument--open::text').get()
            boursomaraItem['highest'] = item.css('span.c-instrument.c-instrument--high::text').get()
            boursomaraItem['lowest'] = item.css('span.c-instrument.c-instrument--low::text').get()
            boursomaraItem['volume'] = item.css('span.c-instrument.c-instrument--totalvolume::text').get().replace(' ', '')
            boursomaraItem['valorization'] = item.css('td.c-table__cell::text').getall()[-1].replace(' ', '')
            boursomaraItem['datetime'] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

            yield boursomaraItem.clean_item()

        
