import scrapy
from scrapy.http import Request
import csv
import urllib2

script_name = 'telegram'
allowed_domains = ['bestoftelegram.com', 'telegram.me', 't.me']
start_urls = ['https://bestoftelegram.com/']
file_name = 'telegram.csv'
what_to_search_list = ['https://telegram.me/', 'https://t.me/']

outfile = open(file_name, "w")
writer = csv.writer(outfile)


class WhatsappScrapySpider(scrapy.Spider):
    name = script_name
    allowed_domains = allowed_domains
    start_urls = start_urls

    def parse(self, response):
        urls = response.xpath('//a/@href').extract()
        for url in urls:
            if len([True for what_to_search in what_to_search_list if str(url).startswith(what_to_search)]) > 0:
                yield Request(response.urljoin(url), callback=self.parse_group, meta={'url': url})
            yield Request(response.urljoin(url), callback=self.parse)

    def parse_group(self, response):
        url = response.meta.get('url')
        try:
            title = response.xpath('//span[contains(@dir, "auto")]/text()').extract_first()
            writer.writerow([url, title])
        except:
            writer.writerow([url])
