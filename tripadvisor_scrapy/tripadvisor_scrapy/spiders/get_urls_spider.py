import scrapy
from tripadvisor_scrapy.settings import start_url, url_save_path


class TripAdvisorURLSpider(scrapy.Spider):
    name = "trip_advisor_urls"

    custom_settings = {
        'ITEM_PIPELINES': {
            'tripadvisor_scrapy.pipelines.ExtractURLToCSV': 300
        },
        'FEEDS': {
            url_save_path: {
                'format': 'csv',
                'overwrite': False
            }
        }
    }

    start_urls = [start_url]

    def parse(self, response):
        for item in response.css('div.RfBGI'):
            yield {
                'url': item.css('a.Lwqic.Cj.b::attr(href)').get()
            }

        next_page = response.xpath('//a[contains(text(), "Next")]/@href').extract_first()
        abs_next_page = f'https://www.tripadvisor.com{next_page}'

        if abs_next_page is not None:
            print(abs_next_page)
            yield scrapy.Request(abs_next_page, callback=self.parse)