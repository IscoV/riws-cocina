# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CocinaItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    scrappy = scrapy.Field()
    description = scrapy.Field()
    categories = scrapy.Field()
    ingredients = scrapy.Field()
    steps = scrapy.Field()
    meal_type = scrapy.Field()
    difficulty = scrapy.Field()
    time = scrapy.Field()
    dinners = scrapy.Field()
    tags = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)

