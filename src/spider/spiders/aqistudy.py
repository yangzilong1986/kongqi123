# -*- coding: utf-8 -*-
import scrapy
import json
from spider.items import HistoryCityItem, HistoryMonthItem, HistoryDayItem


class HistorySpider(scrapy.Spider):
    '''
    scrapy crawl aqistudy -a city_name=上海 -a month=2017-01
    '''
    name = "aqistudy"
    city_name = ''
    month = ''
    allowed_domains = ["aqistudy.cn"]
    start_urls = []
    custom_settings = dict(
        DOWNLOAD_DELAY=2,
        CONCURRENT_REQUESTS_PER_DOMAIN=8,
        CONCURRENT_REQUESTS_PER_IP=8,
        ITEM_PIPELINES={
            'spider.pipelines.HistoryPipeline': 300,
        },
    )

    def __init__(self, city_name, month, *args, **kwargs):
        super(HistorySpider, self).__init__(*args, **kwargs)
        self.city_name = city_name.decode('utf-8')
        self.month = month

        # print args, kwargs
        # if self.jobid:
        #    print "jobid %s" % self.jobid
        # if self._job:
        #    print "_job %s" % self._job

    def start_requests(self):
        if self.city_name and self.month:
            url = 'https://www.aqistudy.cn/historydata/daydata.php?city=%s&month=%s' % (self.city_name, self.month, )
            meta = {'city_name': self.city_name, 'month': self.month}
            return [scrapy.FormRequest(url=url, meta=meta, callback=self.parse_day)]
        else:
            url = 'https://www.aqistudy.cn/historydata/index.php'
            return [scrapy.FormRequest(url=url, callback=self.parse)]

    def parse(self, response):
        '''
        https://www.aqistudy.cn/historydata/index.php
        :param response:
        :return:
        '''
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
        '''
        https://www.aqistudy.cn/historydata/monthdata.php?city=%E4%B8%8A%E6%B5%B7
        :param response:
        :return:
        '''
        city_name = response.meta['city_name']
        month_list = response.xpath('//table[@class="table table-condensed table-bordered table-striped table-hover table-responsive"]//tr[position()>1]')
        if len(month_list) < 1:
            return
        for month in month_list:
            # 处理日期
            month_a = month.xpath('.//a')
            hm_day_url = month_a.xpath('@href').extract_first(default='')

            month_text = month_a.xpath('text()').extract_first()
            if not month_text:
                continue
            month_text = month_text.split(u'-')
            hm_year = 0 if not month_text[0] else month_text[0]
            hm_month = 0 if not month_text[1] else month_text[1]

            hm_aqi = month.xpath('.//td[2]/text()').extract_first(default='0')

            aqi_avg = month.xpath('.//td[3]/text()').extract_first(default='')
            aqi_avg = aqi_avg.split('~')
            hm_aqi_min = '0' if not aqi_avg[0] else aqi_avg[0]
            hm_aqi_max = '0' if not aqi_avg[1] else aqi_avg[1]
            # print "----- aqi_avg: %s, min: %s, max: %s" % (str(aqi_avg), str(hm_aqi_min), str(hm_aqi_max))

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
            yield item

            url = response.urljoin(item['hm_day_url'])
            meta = {'city_name': city_name}
            yield scrapy.Request(url=url, meta=meta, callback=self.parse_day, priority=90)

    def parse_day(self, response):
        '''
        https://www.aqistudy.cn/historydata/daydata.php?city=%E4%B8%8A%E6%B5%B7&month=2017-02
        :param response:
        :return:
        '''
        city_name = response.meta['city_name']
        day_list = response.xpath('//table[@class="table table-condensed table-bordered table-striped table-hover table-responsive"]//tr[position()>1]')
        if len(day_list) < 1:
            return
        for day in day_list:
            hd_date = day.xpath('.//td[1]/text()').extract_first(default='')
            if len(hd_date) < 4:
                continue

            hd_aqi = day.xpath('.//td[2]/text()').extract_first(default='0')

            aqi_avg = day.xpath('.//td[3]/text()').extract_first(default='')
            aqi_avg = aqi_avg.split('~')
            hd_aqi_min = '0' if not aqi_avg[0] else aqi_avg[0]
            hd_aqi_max = '0' if not aqi_avg[1] else aqi_avg[1]
            # print "----- aqi_avg: %s, min: %s, max: %s" % (str(aqi_avg), str(hd_aqi_min), str(hd_aqi_max))

            hd_quality = day.xpath('.//td[4]/div/text()').extract_first(default='')
            hd_pm25 = day.xpath('.//td[5]/text()').extract_first(default='0')
            hd_pm10 = day.xpath('.//td[6]/text()').extract_first(default='0')
            hd_so2 = day.xpath('.//td[7]/text()').extract_first(default='0')
            hd_co = day.xpath('.//td[8]/text()').extract_first(default='0')
            hd_no2 = day.xpath('.//td[9]/text()').extract_first(default='0')
            hd_o3 = day.xpath('.//td[10]/text()').extract_first(default='0')

            hd_rank = day.xpath('.//td[11]/text()').extract_first(default='0')

            item = HistoryDayItem()
            item['city_id'] = 0
            item['city_name'] = city_name.strip()
            item['hd_date'] = hd_date.strip()
            item['hd_aqi'] = float(hd_aqi.strip())
            item['hd_aqi_min'] = float(hd_aqi_min.strip())
            item['hd_aqi_max'] = float(hd_aqi_max.strip())
            item['hd_quality'] = hd_quality.strip()
            item['hd_pm25'] = float(hd_pm25.strip())
            item['hd_pm10'] = float(hd_pm10.strip())
            item['hd_so2'] = float(hd_so2.strip())
            item['hd_co'] = float(hd_co.strip())
            item['hd_no2'] = float(hd_no2.strip())
            item['hd_o3'] = float(hd_o3.strip())
            item['hd_rank'] = int(hd_rank.strip())
            yield item

    def closed(self, reason):
        print '-------------------------spider closed.-----------------------'
        print reason
