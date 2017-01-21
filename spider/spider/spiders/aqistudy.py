# -*- coding: utf-8 -*-
import scrapy
import json
from spider.items import HistoryCityItem, HistoryMonthItem, HistoryDayItem


class HistorySpider(scrapy.Spider):
    name = "aqistudy"
    allowed_domains = ["aqistudy.cn"]
    start_urls = [
        "https://www.aqistudy.cn/historydata/index.php"
    ]
    custom_settings = dict(
        DOWNLOAD_DELAY=2,
        CONCURRENT_REQUESTS_PER_DOMAIN=8,
        CONCURRENT_REQUESTS_PER_IP=8
    )

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

            item = HistoryCityItem()
            item['city_name'] = city_name.strip()
            item['city_url'] = city_url.strip()

            # print '----- HistoryCityItem:%s' % json.dumps(dict(item), indent=4, ensure_ascii=False)
            yield item

            url = response.urljoin(city_url)
            meta = {'city_name': city_name}
            yield scrapy.Request(url=url, meta=meta, callback=self.parse_month, priority=20)

    def parse_month(self, response):
        city_name = response.meta['city_name']
        month_list = response.xpath('//table//tr[position()>1]')
        for month in month_list:
            # 处理日期
            month_a = month.xpath('.//a')
            hm_day_url = month_a.xpath('@href').extract_first(default='')

            month_text = month_a.xpath('text()').extract_first(default='')
            if not month_text:
                continue
            month_text = month_text.split(u'-')
            hm_year = 0 if not month_text[0] else month_text[0]
            hm_month = 0 if not month_text[1] else month_text[1]

            hm_aqi = month.xpath('.//td[2]/text()').extract_first(default='0')

            aqi_avg = month.xpath('.//td[3]/text()').extract_first(default='')
            if not aqi_avg:
                continue
            aqi_avg = aqi_avg.split(u'~')
            hm_aqi_min = 0 if not aqi_avg[0] else aqi_avg[0]
            hm_aqi_max = 0 if not aqi_avg[1] else aqi_avg[1]

            hm_quality = month.xpath('.//td[4]/div/text()').extract_first(default='')
            hm_pm25 = month.xpath('.//td[5]/text()').extract_first(default='0')
            hm_pm10 = month.xpath('.//td[6]/text()').extract_first(default='0')
            hm_so2 = month.xpath('.//td[7]/text()').extract_first(default='0')
            hm_co = month.xpath('.//td[8]/text()').extract_first(default='0')
            hm_no2 = month.xpath('.//td[9]/text()').extract_first(default='0')
            hm_o3 = month.xpath('.//td[10]/text()').extract_first(default='0')

            hm_rank = month.xpath('.//td[11]/text()').extract_first(default='0')

            item = HistoryMonthItem()
            item['city_id'] = 0
            item['city_name'] = city_name.strip()
            item['hm_year'] = int(hm_year.strip())
            item['hm_month'] = int(hm_month.strip())
            item['hm_aqi'] = float(hm_aqi.strip())
            item['hm_aqi_min'] = float(hm_aqi_min.strip())
            item['hm_aqi_max'] = float(hm_aqi_max.strip())
            item['hm_quality'] = hm_quality.strip()
            item['hm_pm25'] = float(hm_pm25.strip())
            item['hm_pm10'] = float(hm_pm10.strip())
            item['hm_so2'] = float(hm_so2.strip())
            item['hm_co'] = float(hm_co.strip())
            item['hm_no2'] = float(hm_no2.strip())
            item['hm_o3'] = float(hm_o3.strip())
            item['hm_rank'] = int(hm_rank.strip())
            item['hm_day_url'] = hm_day_url.strip()

            # print u"----- HistoryMonthItem:%s" % json.dumps(dict(item), indent=4)
            yield item




