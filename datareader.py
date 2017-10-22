import csv
import datetime
import numpy as np

from entities.tweet import Tweet


def ms_str(tw):
    return datetime.datetime.fromtimestamp(tw/1e3).strftime('%Y-%m-%d %H:%M:%S')

rows_to_read = 100

clusters = {}
intermediate_cluster_count = {}
tweets = []
intermediate_tweet_numbers = []
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

        t = Tweet(int(row[2]),
                  int(row[3]),
                  int(row[4]),
                  row[6])

        t.cluster_id = cluster_id

        tweets.append(t)

        intermediate_tweet_numbers.append([t.cluster_id, t.timestamp_ms])

        if cluster_id not in clusters:
            clusters[cluster_id] = cluster_entity
            intermediate_cluster_count[cluster_id] = 0
        intermediate_cluster_count[cluster_id] = intermediate_cluster_count[cluster_id] + 1

tweet_numbers = np.array(intermediate_tweet_numbers)

cluster_time_centroids = []

for c in clusters:
    if intermediate_cluster_count[c] > 100:
        filtered_clusters.add(c)
        cc = int(np.mean(tweet_numbers[tweet_numbers[:,0] == c][:,1]))

        print(c, ms_str(cc))