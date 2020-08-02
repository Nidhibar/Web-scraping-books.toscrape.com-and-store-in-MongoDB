# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# class QuotesSpiderPipeline:
#     def process_item(self, item, spider):
#         return item
from pymongo import MongoClient
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

class MongoDBPipeline(object):
	def __init__(self):
		connection=MongoClient(
			settings['MONGODB_SERVER'],
			settings['MONGODB_PORT'])
		db=connection[settings['MONGODB_DB']]
		self.collection=db[settings['MONGODB_COLLECTION']]

	def process_item(self,item,spider):
	 	self.collection.insert(dict(item))
	 	return item