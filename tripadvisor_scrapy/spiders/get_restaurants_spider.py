import scrapy
import pandas as pd
from tripadvisor_scrapy.settings import restaurant_save_path, url_save_path


class TripAdvisorRestaurantSpider(scrapy.Spider):
    """
    Gets all the restaurant information from each individual page.

    """

    name = "trip_advisor_restaurants"

    custom_settings = {
        "ITEM_PIPELINES": {"tripadvisor_scrapy.pipelines.ExtractRestaurantToCSV": 800},
        "FEEDS": {restaurant_save_path: {"format": "csv", "overwrite": False}},
    }

    start_urls = pd.read_csv(url_save_path)["url"].unique().tolist()

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