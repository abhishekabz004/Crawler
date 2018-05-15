# -*- coding: utf-8 -*-

import scrapy
import hashlib
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class AmazonPipeline(ImagesPipeline):

	# Name thumbnail version
	def thumb_path(self, request, thumb_id, response=None, info=None):
		image_guid = thumb_id + response.url.split('/')[-1]
		return 'thumbs/%s/%s.jpg' % (thumb_id, image_guid)

	def file_path(self, request, response=None, info=None):
		return request.meta.get('filename', '')

	def get_media_requests(self, item, info):
		meta = {'filename': item['image_paths']}
		for image_url in item['image_urls']:
			yield scrapy.Request(url=image_url, meta = meta)

	def item_completed(self, results, item, info):
		image_paths = [x['path'] for ok, x in results if ok]
		if not image_paths:
			raise DropItem("Item contains no images")
			item['image_paths'] = image_paths
			return item


class FlipkartPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        image_path = request.meta['page_url'][:request.meta['page_url'].rfind('/')]
        image_path = image_path[image_path.rfind('/') + len('/'):]
        image_guid = '/flipkart/'+ image_path + '/' + hashlib.sha1(request.url).hexdigest() +'.jpg'
        return image_guid

    def get_media_requests(self, item, info):
        yield scrapy.Request(item['image_urls'][0], meta=item)
