import scrapy
import os

class ProductSpider(scrapy.Spider):
    # Spider name
    name = 'product'
     # Allowed domains for this spider
    allowed_domains = ['web-scraping.dev']
    # Maximum number of pages to crawl
    max_pages = 99
     # Maximum depth of the crawl
    max_depth = 9

    def start_requests(self):
         # Starting URL for the crawl
        url = getattr(self, 'url', None)
        if url:
             # Loop through the page numbers
            for page_number in range(1, self.max_pages + 1):
                 # Yield a new request for each page
                yield scrapy.Request(f'{url}{page_number}', self.parse, meta={'depth': 1})

    def parse(self, response):
         # Check if the maximum depth has been reached
        if response.meta.get('depth', 0) > self.max_depth:
            # If so, return and stop crawling
            return
# Extract the product name from the page
        product_name = response.css('title::text').get()
         # Extract the product ID from the URL
        prod = response.url.split('/')[-1].split('.')[0].split('-')[-1]
         # Construct the product link
        link = f'https://web-scraping.dev/product/{prod}'
 # Yield a dictionary with the product information
        yield {
            'title': product_name,
            'link': link
        }
 # Save the HTML response to a file
        filename = 'crawler/product/product-' + response.url.split('/')[-1] + '.html'
        success = True

        if success:
            # Open the file in write mode
            with open(filename, 'wb') as f:
                 # Write the response body to the file
                f.write(response.body)
                 # Log a message indicating the file was saved
            self.log(f'Saved file {filename}')

class HTMLSpider(scrapy.Spider):
    name = 'html_spider'
      # Starting URLs for the crawl
    start_urls = [f'file://{"C:/info2/crawler/crawler"}/product/{c}' for c in os.listdir('crawler/product')]

    def parse(self, response):
        title = response.css('title::text').get()
        prod = response.url.split('/')[-1].split('.')[0].split('-')[-1]
        link = f'https://web-scraping.dev/product/{prod}'

        yield {
            'title': title,
            'link': link
        }
