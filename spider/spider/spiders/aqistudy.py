# -*- coding: utf-8 -*-
import scrapy
from spider.items import CitiesItem


class HistorySpider(scrapy.Spider):
    name = "history"
    allowed_domains = ["aqistudy.cn"]
    start_urls = [
        "https://www.aqistudy.cn/historydata/index.php"
    ]

    def __init__(self, *args, **kwargs):
        super(HistorySpider, self).__init__(*args, **kwargs)

    def parse(self, response):

        city_list = response.xpath('//div[@class="all"]//li//a')
        # print "city_list: %s" % str(city_list)

        for city in city_list:
            city_name = city.xpath('text()').extract()
            city_url = city.xpath('@href').extract()

            city_name = city_name[0].encode('utf-8')
            city_url = city_url[0].encode('utf-8')

            print "cities: %s, url: %s " % (city_name, city_url)

            yield scrapy.Request(url=city_url,
                                 meta={'city_name': city_name},
                                 callback=self.parse_month,
                                 priority=20)
            """
            item = CitiesItem()
            item['city_name'] = city_name
            item['city_url'] = city_url
            yield item
            """

    def parse_month(self, response):
        month_list = response.xpath('//table//tr[position()>1]')
        for month in month_list:
            # 处理日期
            month_a = month.xpath('//a')
            hm_day_url = month_a.xpath('@href').extract_first()
            month_text = month_a.xpath('text()').extract_first()
            month_text = month_text.split(u'-')
            hm_year = month_text[0]
            hm_month = month_text[1]

            hm_aqi = month.xpath('//td[2]/text()').extract_first()

            aqi_avg = month.xpath('//td[3]/text()').extract_first()
            aqi_avg = aqi_avg.split(u'~')
            hm_aqi_min = aqi_avg[0]
            hm_aqi_max = aqi_avg[1]

            hm_quality = month.xpath('//td[4]/text()').extract_first()
            hm_pm25 = month.xpath('//td[5]/text()').extract_first()
            hm_pm10 = month.xpath('//td[6]/text()').extract_first()
            hm_so2 = month.xpath('//td[7]/text()').extract_first()
            hm_co = month.xpath('//td[8]/text()').extract_first()
            hm_no2 = month.xpath('//td[9]/text()').extract_first()
            hm_o3 = month.xpath('//td[10]/text()').extract_first()

            hm_rank = month.xpath('//td[11]/text()').extract_first()





