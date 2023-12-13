import datetime
from typing import Any, Iterable, Optional
import scrapy
from scrapy.http import Request
from ..items import BoursoramaItem
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from ..models.boursorama import Boursorama
from ..models.base import Base

def save_boursama_item(boursorama_item : BoursoramaItem):
    engine = create_engine('sqlite:///sqlite.db', echo=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        boursorama = Boursorama(
            boursorama_item['label'],
            boursorama_item['last'],
            boursorama_item['variation'],
            boursorama_item['opening'],
            boursorama_item['highest'],
            boursorama_item['lowest'],
            boursorama_item['volume'],
            boursorama_item['valorization'],
            boursorama_item['datetime']
        )
        session.add(boursorama)
        session.commit()

    engine.dispose()


class BoursoramaSpider(scrapy.Spider):
    name = "boursorama"
    allowed_domains = ["www.boursorama.com"]
        
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
            boursomaraItem['volume'] = item.css('span.c-instrument.c-instrument--totalvolume::text').get().replace(' ', '').replace(',', '')
            boursomaraItem['valorization'] = item.css('td.c-table__cell::text').getall()[-1].replace(' ', '').replace(',', '')
            boursomaraItem['datetime'] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

            save_boursama_item(boursomaraItem)

            yield boursomaraItem.clean_item()

        
