# -*- coding: utf-8 -*-
from datetime import date

import scrapy
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from cocina.items import CocinaItem
from cocina.utils import clear_spaces, first_or_none, n_or_none


class CookingclassySpider(CrawlSpider):
    name = 'cookingclassy'
    allowed_domains = ['cookingclassy.com']
    start_urls = [
        'https://www.cookingclassy.com/recipes/appetizer/',
        'https://www.cookingclassy.com/recipes/asian/',
        'https://www.cookingclassy.com/recipes/meat/',
        'https://www.cookingclassy.com/recipes/bread/',
        'https://www.cookingclassy.com/recipes/breakfast/',
        'https://www.cookingclassy.com/recipes/bars/',
        'https://www.cookingclassy.com/recipes/cake/',
        'https://www.cookingclassy.com/recipes/cookies/',
        'https://www.cookingclassy.com/recipes/dessert/',
        'https://www.cookingclassy.com/recipes/healthy/',
        'https://www.cookingclassy.com/recipes/fall-faves/',
        'https://www.cookingclassy.com/recipes/drinks/',
        'https://www.cookingclassy.com/recipes/holidays/',
        'https://www.cookingclassy.com/recipes/ice-cream/',
        'https://www.cookingclassy.com/recipes/instant-pot/',
        'https://www.cookingclassy.com/recipes/muffins/',
        'https://www.cookingclassy.com/recipes/mexican/',
        'https://www.cookingclassy.com/recipes/main-dish/',
        'https://www.cookingclassy.com/recipes/italian/',
        'https://www.cookingclassy.com/recipes/pie-cheesecake/',
        'https://www.cookingclassy.com/recipes/poultry/',
        'https://www.cookingclassy.com/recipes/side/',
        'https://www.cookingclassy.com/recipes/seafood/',
        'https://www.cookingclassy.com/recipes/sandwich/',
        'https://www.cookingclassy.com/recipes/slow-cooker/',
        'https://www.cookingclassy.com/recipes/soup/',
        'https://www.cookingclassy.com/recipes/tarts-and-pastries/',
        'https://www.cookingclassy.com/recipes/treats/',
        'https://www.cookingclassy.com/recipes/uncategorized/'
    ]

    rules = (
        Rule(LxmlLinkExtractor(allow=(), restrict_xpaths=('//a[@class="nextpostslink"]',)),
             callback="parse", follow=True),
    )

    def parse(self, response):
        urls = response.xpath('//div[@class="recipegrid"]/ul/li/a/@href').extract()

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
        yield CocinaItem(
            name=clear_spaces(first_or_none(response.xpath('//h1[@class="title"]/text()').extract())),
            url=response.url,
            scrappy=self.name,
            description=clear_spaces(first_or_none(response.xpath('string(//div[@class="content"]/p)').extract())),
            categories=self.__process_category(
                first_or_none(response.xpath('string(//div[@class="catstags"])').extract())),
            ingredients=self.__process_ingredients(response.xpath('//li[@class="wprm-recipe-ingredient"]')),
            steps=self.__process_steps(response.xpath('//div[@class="wprm-recipe-instruction-text"]')),
            tags=self.__process_tags(
                first_or_none(response.xpath('string(//div[@class="catstags"])').extract())),
            meal_type=first_or_none(response.xpath('//p[@id="breadcrumbs"]/span/span/span/a/text()').extract()),
            difficulty=None,
            time=self.__process_time((first_or_none(response.xpath(
                'string(//div[@class="wprm-recipe-total-time-container"])').extract()))),
            dinners=self.__process_dinners((first_or_none(response.xpath(
                'string(//span[@class="wprm-recipe-details wprm-recipe-servings"])').extract()))),
            last_updated=self.__process_update(
                clear_spaces(first_or_none(response.xpath('//div[@class="date"]/text()').extract()))),
            language='en',
        )

    @staticmethod
    def __process_category(category):
        category = clear_spaces(first_or_none(category.split('Tagged:')))
        if not category:
            return None
        category = category.replace('Categorized:', '')
        return [clear_spaces(e) for e in category.split(',')]

    @staticmethod
    def __process_tags(tags):
        tags = clear_spaces(n_or_none(tags.split('Tagged:'), 1))
        if not tags:
            return None
        return [clear_spaces(e) for e in tags.split(',')]

    @staticmethod
    def __process_ingredients(ingredients):
        return [clear_spaces(el.xpath('string()').extract()[0]) for el in ingredients]

    @staticmethod
    def __process_steps(steps):
        return [clear_spaces(el.xpath('string()').extract()[0]) for el in steps]

    @staticmethod
    def __process_time(time):
        if time:
            time = time.replace('Total Time:', '')
        if 'hour' in time and 'minute' in time:
            time = time.replace('hours', '').replace('hour', '').replace('minutes', '').replace('minute', '')
            hour, minute = time.split()[0], time.split()[1]
            return int(hour) * 60 + int(minute)
        if 'hour' in time:
            hour = time.replace('hours', '').replace('hour', '')
            return int(hour) * 60
        if 'minute' in time:
            minute = time.replace('minutes', '').replace('minute', '')
            return int(minute.replace('minutes', ''))
        return None

    @staticmethod
    def __process_dinners(servings):
        return int(servings) if servings else None

    @staticmethod
    def __process_update(d):
        d = d.split('.')
        return date(year=int(d[2]), month=int(d[0]), day=int(d[1]))
