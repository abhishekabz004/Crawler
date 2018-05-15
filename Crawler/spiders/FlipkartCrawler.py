import scrapy

from ..items import FlipkartItem
import json, csv, os
import hashlib

class FlipkartcrawlerSpider(scrapy.Spider):
    name = "FlipkartCrawler"
    custom_settings = {
        'ITEM_PIPELINES': {
            'Crawler.pipelines.FlipkartPipeline': 1
        }
    }
    # enter the urls to crawl as a list here
    start_urls = ['https://www.flipkart.com/sarees/pr?otracker=nmenu_sub_Women_0_Sarees&otracker=nmenu_sub_Women_0_Sarees&page=50&sid=2oq%2Cc1r%2C3pj%2C7od&viewType=grid']
    item_id = 1
    page_number = 0

    def parse(self, response):
        # get contents in script tag which has media in it
        self.page_number = response.url[response.url.find('page=')+len('page='):response.url.rfind('&sid')]
        csv_file_name = response.url[:response.url.rfind('/')]
        csv_file_name = csv_file_name[csv_file_name.rfind('/')+len('/'):]
        if not os.path.exists('/datasets'):
            os.makedirs('datasets')
        csv_file_name = 'datasets/flipkart_' + csv_file_name.replace('/', '_') + '.csv'
        data = response.xpath("//script[contains(., 'media')]/text()").extract_first()
        if data is not None:
            data = data.encode('utf-8')
            data = data.replace('"apiError":{}};\n', '"apiError":{}}')
            data = data.replace('window.__INITIAL_STATE__ = ', '')

            # convert the string to Json object
            raw_json = json.loads(data)
            raw_json = self.convert_keys_to_string(raw_json)

            # write the crawled data to a csv file
            with open(csv_file_name, 'a') as csvfile:
                fieldnames = ['id', 'page_number', 'flipkart_product_id', 'title', 'key_specs', 'analytics_data', 'rating',
                              'file_name', 'url']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if os.stat(csv_file_name).st_size == 0:
                    writer.writeheader()
                for product in raw_json['productSummary']:
                    try:
                        images_list = raw_json['productSummary'][product]['value']['media']['images']
                        flipkart_item_id = raw_json['productSummary'][product]['value']['itemId']
                        title = raw_json['productSummary'][product]['value']['titles']['title']
                        key_specs = raw_json['productSummary'][product]['value']['keySpecs']
                        analytics_data = raw_json['productSummary'][product]['value']['analyticsData']
                        rating = raw_json['productSummary'][product]['value']['rating']
                        for image in images_list:
                            image = self.convert_keys_to_string(image)
                            # replace the width, height and quality fields in the url
                            image_url = image['url'].encode('utf-8').replace('{@width}', '300')
                            image_url = image_url.encode('utf-8').replace('{@height}', '300')
                            image_url = image_url.encode('utf-8').replace('{@quality}', '100')
                            hash_object = hashlib.sha1(image_url)
                            hex_dig = hash_object.hexdigest()
                            writer.writerow({'id': self.item_id, 'page_number': self.page_number, 'flipkart_product_id': flipkart_item_id, 'title': title,
                                             'key_specs': key_specs, 'analytics_data': analytics_data, 'rating': rating,
                                             'file_name': str(hex_dig)+'.jpeg', 'url': image_url})
                            # download the images from the url
                            yield FlipkartItem(image_urls=[image_url], page_url=response.url)
                            self.item_id = self.item_id+1
                    except Exception as e:
                        print (e)

            # check if next page is available
            next_page = response.css('div._2kUstJ a::attr(href)').extract()[-1]
            if next_page is not None:
                yield response.follow('https://www.flipkart.com'+next_page, callback=self.parse)

        else:
            print ('========STOPPED COLLECTING DATA========')
            print ('ERROR IN COLLECTING DATA FOR ' + response.request.url)

    def convert_keys_to_string(self, dictionary):
        """Recursively converts dictionary keys to strings."""
        if not isinstance(dictionary, dict):
            return dictionary
        return dict((str(k), self.convert_keys_to_string(v))
            for k, v in dictionary.items())
