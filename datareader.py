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

rows_to_read = 100

clusters = {}
cluster_count = {}
filtered_clusters = set()

with open("data/1day/clusters.sortedby.clusterid.csv", 'r', encoding='utf-8') as reddit_posts_csv:
    reader = csv.reader(reddit_posts_csv, delimiter=',',
                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        # if rows_to_read < 0:
        #     break
        # rows_to_read = rows_to_read - 1
        ################################
        cluster_id = int(row[0])
        cluster_entity = row[1]

        if not cluster_id in clusters:
            clusters[cluster_id] = cluster_entity
            cluster_count[cluster_id] = 0
        cluster_count[cluster_id] = cluster_count[cluster_id] + 1

    for c in clusters:
        if cluster_count[c] > 100:
            filtered_clusters.add(c)

    print(len(filtered_clusters))
