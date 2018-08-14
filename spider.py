import scrapy


class Spider(scrapy.Spider):
    name = 'wallpapers page spider'
    start_urls = ['file:///home/pbodyachevsky/PycharmProjects/untitled/wallpapers.html']

    def parse(self, response):
        div_with_wallpapers = response.css('.c-garfield-the-cat').extract()
        print(div_with_wallpapers)