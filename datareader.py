import csv
import datetime
import numpy as np

from entities.tweet import Tweet


def ms_str(tw):
    return datetime.datetime.fromtimestamp(tw/1e3).strftime('%Y-%m-%d %H:%M:%S')


cluster_filter_threshold = 100

clusters = {}
intermediate_cluster_count = {}
tweets = []
intermediate_tweet_numbers = []

with open("data/1day/clusters.sortedby.clusterid.csv", 'r', encoding='utf-8') as reddit_posts_csv:
    reader = csv.reader(reddit_posts_csv, delimiter=',',
                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        cluster_id = int(row[0])
        cluster_entity = row[1]
        timestamp_ms = int(row[3])

        # t = Tweet(int(row[2]),
        #           timestamp_ms,
        #           int(row[4]),
        #           row[6])
        # t.cluster_id = cluster_id
        # tweets.append(t)

        intermediate_tweet_numbers.append([cluster_id, timestamp_ms])

        if cluster_id not in clusters:
            clusters[cluster_id] = cluster_entity
            intermediate_cluster_count[cluster_id] = 0
        intermediate_cluster_count[cluster_id] = intermediate_cluster_count[cluster_id] + 1

tweet_numbers = np.array(intermediate_tweet_numbers)

# filter out small clusters
filtered_clusters = set()
relevant_cluster_centroids = []
cluster_entities = {}

for c_id in clusters:
    if intermediate_cluster_count[c_id] > cluster_filter_threshold:
        filtered_clusters.add(c_id)
        timestamp_centroid = int(np.mean(tweet_numbers[tweet_numbers[:, 0] == c_id][:, 1]))
        cluster_entities[c_id] = set(clusters[c_id].split(' '))
        relevant_cluster_centroids.append([c_id, timestamp_centroid ])

relevant_cluster_centroids = np.array(relevant_cluster_centroids)
centroids_sortedby_time = relevant_cluster_centroids[relevant_cluster_centroids[:, 1].argsort()]

# find similar clusters:
candidate_similar_clusters = {}
window_timedelta = datetime.timedelta(hours=1)
window_timespan = window_timedelta.total_seconds() * 1000

# o(n^2) algorithm, needs improvement
for centroid in centroids_sortedby_time:
    cluster_id = centroid[0]
    window_start = centroid[1] - window_timespan
    window_end = centroid[1]
    for centroid_ in centroids_sortedby_time: # search again from the begining
        other_cluster_id = centroid_[0]
        if window_start >= centroid_[1] or centroid_[1] > window_end or cluster_id == other_cluster_id:
            continue # continue if its outside our time window

        if cluster_id not in candidate_similar_clusters:
            candidate_similar_clusters[cluster_id] = []

        overlap = cluster_entities[cluster_id].intersection(cluster_entities[other_cluster_id])
        if len(overlap) > 0:
            candidate_similar_clusters[cluster_id].append(other_cluster_id)

for cluster_id in candidate_similar_clusters:
    if len(candidate_similar_clusters[cluster_id]) == 0:
        continue
    print(clusters[cluster_id] + ":")
    for candidate in candidate_similar_clusters[cluster_id]:
        print("\t",clusters[candidate])
