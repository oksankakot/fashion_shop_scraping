import csv
import json
import re

import scrapy
from scrapy.http import Response


class FarfetchSpider(scrapy.Spider):
    name = "farfetch"
    allowed_domains = ["farfetch.com"]
    start_urls = ["https://www.farfetch.com/ca/shopping/women/dresses-1/items.aspx"]

    def __init__(self, *args, **kwargs):
        super(FarfetchSpider, self).__init__(*args, **kwargs)
        self.parsed_items = 0
        self.max_items = 130

    def parse(self, response: Response, **kwargs):
        product_links = response.css(
            'li[data-testid="productCard"] div[data-component="ProductCard"]::attr(itemid)').getall()
        for link in product_links:
            yield response.follow(link, callback=self.parse_product)

        next_page = "https://www.farfetch.com/ca/shopping/women/dresses-1/items.aspx?page=2&view=96&sort=3"
        yield scrapy.Request(next_page, callback=self.parse)

    def parse_product(self, response: Response):
        product_id = response.css("p:contains('FARFETCH ID:')").css("span::text").get().strip(),
        item_group_id = response.css("p:contains('Brand style ID:')").css("span::text").get().strip(),
        mpn = response.css("p:contains('Brand style ID:')").css("span::text").get().strip(),

        gtin = response.css('[itemprop="gtin13"]::text').get()
        description = response.css('title::text').get()
        title = response.css('p.ltr-4y8w0i-Body::text').get()

        image_link = response.css('meta[property="og:image"]::attr(content)').get()
        additional_image_links = response.css('img::attr(src)').getall()
        link = response.css('meta[property="og:url"]::attr(content)').get()
        gender = response.xpath(
            'normalize-space(//script[contains(text(), "window.universal_variable")]/text())').re_first(
            r'"name":"(.*?)"')
        age_group = "adult"
        price = response.css('p[data-component="PriceLarge"]::text').get()

        json_data = response.css('script[type="application/ld+json"]::text').get()
        data = json.loads(json_data)
        brand = data.get('brand', {}).get('name')
        color = data.get('color')
        availability = data.get('offers', {}).get('availability')

        if availability == 'https://schema.org/InStock':
            availability = 'in_stock'
        else:
            availability = 'out_of_stock'

        sizes_pattern = re.compile(r'\b(?:XXS|XS|S|M|L|XL|XXL|XXXL)\b')
        available_sizes = list(set(sizes_pattern.findall(response.text)))

        yield {
            'id': product_id,
            'item_group_id': item_group_id,
            'mpn': mpn,
            'gtin': gtin,
            'title': title,
            'description': description,
            'image_link': image_link,
            'additional_image_links': additional_image_links,
            'link': link,
            'gender': gender,
            'age_group': age_group,
            'brand': brand,
            'color': color,
            'availability': availability,
            'size': available_sizes,
            'price': price,
            'product_type': self._get_product_type(response),
            'condition': None
        }

    @staticmethod
    def _get_product_type(response: Response) -> str:
        product_types_li_elements = response.css('ol[data-component="Breadcrumbs"] li')

        return " ".join([
            f"{li_product_type.css('a::text').get()};"
            for li_product_type in product_types_li_elements
        ])

    def get_google_product_category(self, product_type):
        last_word = product_type.split()[-1]

        with open('C:\\Users\\User\\test_task\\fashion_scraping\\farfetch_scraper\\cats.csv', newline='',
                  encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0].split(';')[0] == last_word:
                    return row
        return None
