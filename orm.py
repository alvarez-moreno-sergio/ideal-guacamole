from bson import ObjectId
from pymongo import MongoClient

class Mongo:

	_client = None

	def init():
		Mongo._client = MongoClient()

	def client():
		return Mongo._client

	def save(collection, detail):
		return collection.insert_one(detail).inserted_id

	def save_dict(collection, content):
		print('Saving collection to Mongo db ...')
		for k in content:
			Mongo.save(collection, content[k].to_hash())
		print('Done.')
