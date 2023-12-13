import scrapy

from WebCrawler.items import AnimeItem
from ..database_function import save_anime_db


class AnimeSpider(scrapy.Spider):
    name = "anime"
    allowed_domains = ["myanimelist.net"]
    start_urls = ["https://myanimelist.net/anime.php?cat=anime&show={}".format(i) for i in range(0, 28500, 50)] # 25850

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        animes = response.css("div.js-categories-seasonal.js-block-list.list tr")[1:]

        for anime in animes:

            animeItem = AnimeItem()

            try:
                animeItem["name"] = anime.css("div.title strong::text").get()
            except:
                animeItem["name"] = "";
            
            try:
                animeItem['link'] = anime.css("div.title a::attr(href)").get()
            except:
                animeItem['link'] = ""

            try:
                animeItem['image'] = anime.css("div.picSurround a img::attr(data-src)").get().split(",")[-1].strip().split(" ")[0]
            except:
                animeItem['image'] = ""

            try:
                animeItem["description"] = anime.css("div.pt4::text").get()
            except:
                animeItem['description'] = ""

            try: 
                tds = anime.css("td::text").getall()

                animeItem["type"] = tds[-3]
                animeItem["episodes"] = tds[-2]
                animeItem["score"] = tds[-1]
            except:
                animeItem["type"] = ""
                animeItem["episodes"] = ""
                animeItem["score"] = None

            animeItem = animeItem.clean()

            if animeItem["score"] == "N/A":
                animeItem["score"] = None

            if animeItem["episodes"] == '-':
                animeItem["episodes"] = 0

            if animeItem["description"] == None:
                animeItem["description"] = ""

            save_anime_db(animeItem, True)

            yield animeItem