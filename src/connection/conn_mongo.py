import pymongo
from src.utils.cfg import mongo_uri

db = pymongo.MongoClient(mongo_uri)

quota_coll = db['wenshu']['quota']