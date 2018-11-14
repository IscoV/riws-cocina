# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from cocina.items import CocinaItem
from cocina.utils import clear_spaces, first_or_none


class RecetasgratisSpider(CrawlSpider):
    name = 'recetasgratis'
    allowed_domains = ['recetasgratis.net']
    start_urls = [
        'https://www.recetasgratis.net/Recetas-de-Aperitivos-tapas-listado_receta-1_1.html',
        'https://www.recetasgratis.net/Recetas-de-Ensaladas-listado_receta-4_1.html',
        'https://www.recetasgratis.net/Recetas-de-Pasta-listado_receta-5_1.html',
        'https://www.recetasgratis.net/Recetas-de-Sopa-listado_receta-6_1.html',
        'https://www.recetasgratis.net/Recetas-de-Verduras-listado_receta-7_1.html',
        'https://www.recetasgratis.net/Recetas-de-Legumbres-listado_receta-8_1.html',
        'https://www.recetasgratis.net/Recetas-de-Arroces-cereales-listado_receta-9_1.html',
        'https://www.recetasgratis.net/Recetas-de-Carne-listado_receta-10_1.html',
        'https://www.recetasgratis.net/Recetas-de-Aves-caza-listado_receta-11_1.html',
        'https://www.recetasgratis.net/Recetas-de-Pescado-listado_receta-12_1.html',
        'https://www.recetasgratis.net/Recetas-de-Mariscos-listado_receta-13_1.html',
        'https://www.recetasgratis.net/Recetas-de-Salsas-guarniciones-listado_receta-14_1.html',
        'https://www.recetasgratis.net/Recetas-de-Cocteles-bebida-listado_receta-15_1.html',
        'https://www.recetasgratis.net/Recetas-de-Pan-bolleria-listado_receta-16_1.html',
        'https://www.recetasgratis.net/Recetas-de-Postres-listado_receta-17_1.html',
        'https://www.recetasgratis.net/Recetas-de-Huevos-lacteos-listado_receta-18_1.html',
        'https://www.recetasgratis.net/Recetas-de-Guisos-Potage-listado_receta-19_1.html',
    ]

    rules = (
        Rule(LxmlLinkExtractor(allow=(), restrict_xpaths=('//a[@class="next ga"]',)), callback="parse", follow=True),
    )

    def parse(self, response):
        urls = response.xpath('//a[@class="titulo titulo--resultado"]/@href').extract()

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
        yield CocinaItem(
            name=clear_spaces(first_or_none(response.xpath('//h1[@class="titulo titulo--articulo"]/text()').extract())),
            url=response.url,
            scrappy=self.name,
            description=clear_spaces(first_or_none(response.xpath('string(//div[@class="intro"]/p)').extract())),
            categories=self.__process_breadcrumb(
                response.xpath('//div[@class="header-gap"]/ul[@class="breadcrumb"]/li/a/span/text()').extract(),
                response.xpath('//div[@class="header-gap"]/ul[@class="breadcrumb"]/li[last()]/text()').extract()),
            ingredients=self.__process_ingredients(response.xpath('//li[@class="ingrediente"]')),
            steps=self.__process_steps(response.xpath('//div[@class="apartado"]/p')),
            tags=self.__process_tags(response.xpath('string(//div[@class="properties inline"])').extract()),
            meal_type=clear_spaces(first_or_none(response.xpath('//span[@class="property para"]/text()').extract())),
            difficulty=clear_spaces(
                first_or_none(response.xpath('//span[@class="property dificultad"]/text()').extract())),
            time=clear_spaces(first_or_none(response.xpath('//span[@class="property duracion"]/text()').extract())),
            dinners=clear_spaces(
                first_or_none(response.xpath('//span[@class="property comensales"]/text()').extract())),
            last_updated=clear_spaces(first_or_none(response.xpath('//span[@class="date_publish"]/text()').extract())),
            language='es',
        )

    @staticmethod
    def __process_description(msg):
        return clear_spaces(msg)

    @staticmethod
    def __process_breadcrumb(bread, last):
        return [clear_spaces(e) for e in bread + last]

    @staticmethod
    def __process_tags(tags):
        return [clear_spaces(e) for e in tags[0].replace('\nCaracter\u00edsticas adicionales:\n', '').split(',')]

    @staticmethod
    def __process_ingredients(ingredients):
        return [clear_spaces(el.xpath('string()').extract()[0]) for el in ingredients]

    @staticmethod
    def __process_steps(steps):
        return [clear_spaces(el.xpath('string()').extract()[0]) for el in steps]
