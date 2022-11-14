import scrapy
import pandas as pd
from tripadvisor_scrapy.settings import restaurant_save_path, url_save_path


def get_starting_urls(filepath: str) -> list:
    return pd.read_csv(filepath)["url"].unique().tolist()


class TripAdvisorRestaurantSpider(scrapy.Spider):
    name = "trip_advisor_restaurants"

    custom_settings = {
        "ITEM_PIPELINES": {"tripadvisor_scrapy.pipelines.ExtractRestaurantToCSV": 800},
        "FEEDS": {restaurant_save_path: {"format": "csv", "overwrite": False}},
    }

    def start_requests(self):
        start_url = get_starting_urls(url_save_path)[0]
        yield scrapy.Request(start_url, meta={'playwright': True})

    def parse(self, response):
        for item in response.css("div.page"):
            yield {
                "name": response.css("h1.HjBfq::text").get(),
                "url": response.url,
                "number": response.css("a.BMQDV._F.G-.wSSLS.SwZTJ::text").get(),
                "reviews": response.css("span.AfQtZ::text").getall(),
                "avg_review": response.css("span.ZDEqb::text").get(),
                "cuisine": response.css("span.DsyBj.DxyfE a.dlMOJ::text").getall(),
                "location": response.css("a.AYHFM::text").get(),
                "category_rating": response.css("div.cNFlb").getall(),
            }
        
        print(f"Processed {response.url}")