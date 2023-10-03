import scrapy
import json

# scrapy shell
# fetch("https://www.songfacts.com/category/type-about")
# response.css('.space-bot a::text').get()
# quit()

f = open('/Users/julianadaikawa/Documents/MBA/TCC/songfacts/topics.json')
data = json.load(f)

links = []

for row in data:
    links.append(row['link'])

# f.close()

class SongsSpider(scrapy.Spider):
    name = "songs_topic"
    start_urls = links
    
    def parse(self, response):
        for category in response.css('.space-bot li'):
            yield{
                'topic': response.css('.sub-header h3::text').get(),
                'name': category.css(' a::text').get(),
                'artist': category.css(' li::text').get()[3:] 
                }