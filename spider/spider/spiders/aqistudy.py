import scrapy
from spider.items import CitiesItem


class CitiesSpider(scrapy.Spider):
    name = "cities"
    allowed_domains = ["aqistudy.cn"]
    start_urls = [
        "https://www.aqistudy.cn/historydata/index.php"
    ]

    def parse(self, response):

        city_list = response.xpath('//div[@class="all"]//li//a')
        # print "city_list: %s" % str(city_list)

        for city in city_list:
            city_name = city.xpath('text()').extract()
            city_url = city.xpath('@href').extract()

            city_name = city_name[0].encode('utf-8')
            city_url = city_url[0].encode('utf-8')

            print "cities: %s, url: %s " % (city_name, city_url)

            item = CitiesItem()
            item['city_name'] = city_name
            item['city_url'] = city_url
            yield item

#
# class MonthSpider(scrapy.Spider):
#
#    def __init__(self, *args, **kwargs):
#        super(MonthSpider, self).__init__(*args, **kwargs)
#
#        # self.start_urls = ['http://www.example.com/categories/%s' % category]
#
#    def parse(self, response):
#        pass
#