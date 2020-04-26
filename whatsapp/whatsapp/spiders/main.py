import scrapy
from scrapy.http import Request
import csv
import urllib2

script_name = 'whatsapp'
allowed_domains = ['whatsappgroups.app', 'chat.whatsapp.com']
start_urls = ['https://whatsappgroups.app/']
file_name = 'data.csv'
what_to_search = 'https://chat.whatsapp.com/invite'

outfile = open(file_name, "w")
writer = csv.writer(outfile)


class BooksScrapySpider(scrapy.Spider):
    name = script_name
    allowed_domains = allowed_domains
    start_urls = start_urls

    def parse(self, response):
        urls = response.xpath('//a/@href').extract()
        for url in urls:
            if str(url).startswith(what_to_search):
                yield Request(response.urljoin(url), callback=self.parse_group, meta={'url': url})
            yield Request(response.urljoin(url), callback=self.parse)

    def parse_group(self, response):
        url = response.meta.get('url')
        try:
            title = response.xpath('//h2/text()').extract_first()
            if 'Looks like you don\'t have WhatsApp installed!' in title:
                writer.writerow([url])
            else:
                writer.writerow([url, title])
        except:
            writer.writerow([url])
