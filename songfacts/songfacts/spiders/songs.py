import scrapy

# scrapy shell
# fetch("https://www.songfacts.com/category/type-about")
# response.css('.space-bot a::text').get()
# quit()

class SongsSpider(scrapy.Spider):
    name = "songs"
    # allowed_domains = ["songfacts.com"]
    start_urls = ["https://www.songfacts.com/category/type-about"]

    def parse(self, response):

        for category in response.css('.space-bot a'):
            yield{
                'name': category.css('::text').get(),
                'link': 'https://www.songfacts.com'+category.css('::attr(href)').get()
            }

