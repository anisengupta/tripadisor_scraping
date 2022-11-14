# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from tripadvisor_scrapy.settings import start_url
from urllib.parse import urlparse
import re


def cleanhtml(raw_html):
    CLEANR = re.compile("<.*?>")
    cleantext = re.sub(CLEANR, "", raw_html)
    return cleantext


class ExtractURLToCSV(object):
    def process_item(self, item, spider):
        urls = "https://" + urlparse(start_url).netloc + dict(item)['url']

        return {'url': urls}


class ExtractRestaurantToCSV(object):
    def process_item(self, item, spider):
        names = dict(item)['name']
        urls = dict(item)['url']
        numbers = dict(item)['number']
        reviews = " ".join(dict(item)['reviews'])
        avg_reviews = dict(item)['avg_review']
        cuisine = " ".join(dict(item)['cuisine'])
        location = dict(item)['location']
        category_rating = cleanhtml(" ".join(dict(item)['category_rating']))

        return {
            'name': names,
            'url': urls,
            'number': numbers,
            'reviews': reviews,
            'avg_review': avg_reviews,
            'cuisine': cuisine,
            'location': location,
            'category_rating': category_rating
            }