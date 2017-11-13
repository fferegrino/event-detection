from pymongo import MongoClient
from datetime import datetime
import time
import pymongo

client = MongoClient('localhost', 27017)
db = client['twitter_db']
collection = db['twitter_collection']

accounts = \
    [
        'Isidrocorro',
        'Peaton_No',
        'ApoyoVial',
        'AA_DF',
        'OVIALCDMX',
        '072AvialCDMX',
        'GobCDMX',
        'UCS_CDMX'
    ]

data = collection.find(
        {
            'entities.user_mentions.screen_name': { '$in' : accounts},
            'retweeted_status': {'$exists' : False},
            'created_at_ms': {'$lte': 1509926401}
        },
        {
            "text":1,
            "retweeted_status": 1,
            "created_at":1,
            "_id": 0
        }
    ).sort([("created_at", pymongo.ASCENDING)])

for d in data:

    date = datetime.strptime(d["created_at"],'%a %b %d %H:%M:%S %z %Y')
    created_at_ms = int(time.mktime(date.timetuple()))
    print(date, d["text"])
    #collection.update({"_id": d["_id"]}, {"$set": {"created_at_ms": created_at_ms}})

# {created_at_ms: {$gte: 1510099200}, created_at_ms: {$lte: 1510185599}}
# {created_at_ms :1, created_at : 1}