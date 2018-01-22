from pymongo import MongoClient

class SpiderPipeline(object):

	def __init__(self):
		self.client = MongoClient('localhost',27017)
		self.db = self.client['test']

	def process_item(self, item, spider):
		if spider.name == 'user':
			data = {
				'name': item['name'],
				'avatar': item['avatar'],
				'dec': item['dec'],
				'work_time': item['work_time'],
				'work_price': item['work_price'],
				'address': item['address'],
				'work_list': item['work_list'],
				'edu_list': item['edu_list'],
				'skill_list': item['skill_list'],
				'works': item['works']
			}
			self.db['people'].insert_one(data)

		if spider.name == 'juejin':
			data = {
				'objectId': item['objectId'],
				'title': item['title'],
				'dec': item['dec'],
				'time': item['time'],
				'utime': item['utime'],
				'tag': item['tag'],
				'content': item['content']
			}
			self.db['article'].insert_one(data)

		return item

	def close_spider(self, spider):
		self.db['article'].distinct("objectId")
		patents = {}
		count = 0
		for patent_record in self.db['article'].find({"objectId":{"$ne":0}}):
			if patent_record['objectId'] not in patents.keys():
				patents[patent_record['objectId']] = patent_record
			else:
				count += 1
				self.db['article'].delete_one({"objectId":patent_record['objectId']})
		self.client.close()
