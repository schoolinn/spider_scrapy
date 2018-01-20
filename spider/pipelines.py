from pymongo import MongoClient

class SpiderPipeline(object):

	def __init__(self):
		self.client = MongoClient('localhost',27017)
		self.db = self.client['test']

	def process_item(self, item, spider):
		if spider.name == 'user':
			data = {
				'name': item['name'],
				'url': item['url']
			}
			self.db['people'].insert_one(data)
			return item

		pass

	def close_spider(self, spider):
		self.client.close()
