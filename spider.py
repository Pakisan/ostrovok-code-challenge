import json

import scrapy

import page_parser
import storage
import wallpapers_parser


class Spider(scrapy.Spider):
    name = 'wallpapers page spider'
    start_urls = [
        'https://www.smashingmagazine.com/category/wallpapers/',
        'https://www.smashingmagazine.com/category/wallpapers/page/2/',
        'https://www.smashingmagazine.com/category/wallpapers/page/3/',
        'https://www.smashingmagazine.com/category/wallpapers/page/4/',
        'https://www.smashingmagazine.com/category/wallpapers/page/5/',
        'https://www.smashingmagazine.com/category/wallpapers/page/6/',
        'https://www.smashingmagazine.com/category/wallpapers/page/7/',
        'https://www.smashingmagazine.com/category/wallpapers/page/8/',
        'https://www.smashingmagazine.com/category/wallpapers/page/9/',
        'https://www.smashingmagazine.com/category/wallpapers/page/10/',
        'https://www.smashingmagazine.com/category/wallpapers/page/11/',
    ]

    def parse(self, response):
        wallpapers_collection_page_paths = response.xpath('//article/h1/a/@href').extract()

        for page_path in wallpapers_collection_page_paths:
            url = response.urljoin(page_path)

            if 'wallpaper' in url:
                yield scrapy.Request(url, self.handle_page)

    def handle_page(self, response):
        html = response.body.decode("utf-8")
        wallpapers_nodes = page_parser.parse_page(html)
        date = page_parser.extract_date(html)
        wallpapers = wallpapers_parser.parse_wallpapers(wallpapers_nodes)

        for wallpaper in wallpapers:
            wallpaper.year = date['year']
            wallpaper.month = date['month']

        storage.create()
        storage.save(wallpapers)