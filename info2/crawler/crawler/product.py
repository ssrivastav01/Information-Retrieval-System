import scrapy
import os

class ProductSpider(scrapy.Spider):
    name = 'product'
    allowed_domains = ['web-scraping.dev']
    max_pages = 99
    max_depth = 9

    def start_requests(self):
        url = getattr(self, 'url', None)
        if url:
            for page_number in range(1, self.max_pages + 1):
                yield scrapy.Request(f'{url}{page_number}', self.parse, meta={'depth': 1})

    def parse(self, response):
        if response.meta.get('depth', 0) > self.max_depth:
            return

        product_name = response.css('title::text').get()
        prod = response.url.split('/')[-1].split('.')[0].split('-')[-1]
        link = f'https://web-scraping.dev/product/{prod}'

        yield {
            'title': product_name,
            'link': link
        }

        filename = 'crawler/product/product-' + response.url.split('/')[-1] + '.html'
        success = True

        if success:
            with open(filename, 'wb') as f:
                f.write(response.body)
            self.log(f'Saved file {filename}')

class HTMLSpider(scrapy.Spider):
    name = 'html_spider'
    start_urls = [f'file://{"C:/info2/crawler/crawler"}/product/{c}' for c in os.listdir('crawler/product')]

    def parse(self, response):
        title = response.css('title::text').get()
        prod = response.url.split('/')[-1].split('.')[0].split('-')[-1]
        link = f'https://web-scraping.dev/product/{prod}'

        yield {
            'title': title,
            'link': link
        }