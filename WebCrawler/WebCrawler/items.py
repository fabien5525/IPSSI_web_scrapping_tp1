import scrapy

class BoursoramaItem(scrapy.Item):
    label = scrapy.Field()
    last = scrapy.Field()
    variation = scrapy.Field()
    opening = scrapy.Field()
    highest = scrapy.Field()
    lowest = scrapy.Field()
    volume = scrapy.Field()
    valorization = scrapy.Field()
    datetime = scrapy.Field()

    def clean_item(self):
        for key, value in self.items():
            if isinstance(value, str):
                self[key] = value.strip().replace('\n', '')
            elif isinstance(value, list):
                self[key] = [item.strip() for item in value]
        return self
