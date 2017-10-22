# clusters.sortedby.clusterid

# cluster_id
# cluster_name_entity
# tweet_id
# timestamp_ms
# user_id
# tweet_tokens
# tweet_text

import csv

class ClusteredTweet:
    def __init__(self):
        self.tweet_id


with open("clusters.sortedby.clusterid.csv", 'r', encoding='utf-8') as reddit_posts_csv:
    reader = csv.reader(reddit_posts_csv, delimiter=',',
                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in reader[:5]:
        print(row)
