# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HistoryCityItem(scrapy.Item):
    city_name = scrapy.Field()
    city_url = scrapy.Field()


class HistoryMonthItem(scrapy.Item):
    city_id = scrapy.Field()
    city_name = scrapy.Field()
    hm_year = scrapy.Field()
    hm_month = scrapy.Field()
    hm_aqi = scrapy.Field()
    hm_aqi_min = scrapy.Field()
    hm_aqi_max = scrapy.Field()
    hm_quality = scrapy.Field()
    hm_pm25 = scrapy.Field()
    hm_pm10 = scrapy.Field()
    hm_so2 = scrapy.Field()
    hm_co = scrapy.Field()
    hm_no2 = scrapy.Field()
    hm_o3 = scrapy.Field()
    hm_rank = scrapy.Field()
    hm_day_url = scrapy.Field()


class HistoryDayItem(scrapy.Item):
    city_id = scrapy.Field()
    city_name = scrapy.Field()
    hd_date = scrapy.Field()
    hd_aqi = scrapy.Field()
    hd_aqi_min = scrapy.Field()
    hd_aqi_max = scrapy.Field()
    hd_quality = scrapy.Field()
    hd_pm25 = scrapy.Field()
    hd_pm10 = scrapy.Field()
    hd_so2 = scrapy.Field()
    hd_co = scrapy.Field()
    hd_no2 = scrapy.Field()
    hd_o3 = scrapy.Field()
    hd_rank = scrapy.Field()
