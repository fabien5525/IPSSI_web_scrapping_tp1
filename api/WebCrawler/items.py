import scrapy

class AnimeItem(scrapy.Item):
    name = scrapy.Field()
    image = scrapy.Field()
    description = scrapy.Field()
    type = scrapy.Field()
    episodes = scrapy.Field()
    score = scrapy.Field()
    members = scrapy.Field()
    link = scrapy.Field()
    
    def clean(self):
        for key in self:
            if isinstance(self[key], str):
                self[key] = self[key].replace('\n', '').strip()
        return self