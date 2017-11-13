from os import listdir
from os.path import isfile, join

import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['twitter_db']
collection = db['twitter_collection']

nl = "$numberLong"

input_folder = "official"

json_files_to_analyze = [f for
                         f in listdir(input_folder)
                            if isfile(join(input_folder, f)) and f.endswith(".json")]

def clean_user(tweet, title = None):
    if "user" in tweet and tweet["user"] != None:
        if not isinstance(tweet["user"]["id"], int):
            tweet["user"]["id"] = int(tweet["user"]["id"][nl])

def clean_replies(tweet, title= None):
    if "in_reply_to_status_id" in tweet and tweet["in_reply_to_status_id"] != None:
        if not isinstance(tweet["in_reply_to_status_id"], int):
            tweet["in_reply_to_status_id"] = int(tweet["in_reply_to_status_id"][nl])

    if "in_reply_to_user_id" in tweet and tweet["in_reply_to_user_id"] != None:
        if not isinstance(tweet["in_reply_to_user_id"], int):
            tweet["in_reply_to_user_id"] = int(tweet["in_reply_to_user_id"][nl])

def clean_entities(tweet, title = None):
    entities_names = ["entities", "extended_entities"]
    media_names = ["hashtags","urls","user_mentions","symbols","media"]
    id_to_clean = ["id", "source_status_id", "source_user_id"]
    if title is not None:
        print("\tCleaning "+title)
    for entities in entities_names:
        if entities in tweet and tweet[entities] != None:
            for media_name in media_names:
                if media_name in tweet[entities]:
                    for media in tweet[entities][media_name]:
                        for id_clean in id_to_clean:
                            if id_clean in media and not isinstance(media[id_clean], int):
                                media[id_clean] = int(media[id_clean][nl])


ii = 1

for j_file in json_files_to_analyze:
    with open(join(input_folder, j_file)) as data_file:
        tweet = json.load(data_file)
        tweet["id"] = int(tweet["id"])
        print("Now:", tweet["id"])

        clean_replies(tweet)

        clean_entities(tweet)

        if "extended_tweet" in tweet:
            extended_tweet = tweet["extended_tweet"]

            clean_entities(extended_tweet)
            clean_user(extended_tweet)
            clean_replies(extended_tweet)


        if "quoted_status_id" in tweet and not isinstance(tweet["quoted_status_id"], int):
            tweet["quoted_status_id"] = int(tweet["quoted_status_id"][nl])

        if "quoted_status" in tweet:
            quoted_status = tweet["quoted_status"]
            if not isinstance(tweet["quoted_status"]["id"], int):
                tweet["quoted_status"]["id"] = int(tweet["quoted_status"]["id"][nl])

            if "quoted_status_id" in quoted_status:
                if not isinstance(quoted_status["quoted_status_id"], int):
                    quoted_status["quoted_status_id"] = int(quoted_status["quoted_status_id"][nl])

            clean_entities(quoted_status)
            clean_user(quoted_status)
            clean_replies(quoted_status)

            if "extended_tweet" in quoted_status:
                other_extended_tweet = quoted_status["extended_tweet"]
                clean_entities(other_extended_tweet)
                clean_user(other_extended_tweet)
                clean_replies(other_extended_tweet)

        tweet["timestamp_ms"]

        clean_user(tweet)

        collection.insert(tweet)
        print("Inserted", ii)
        ii = ii + 1