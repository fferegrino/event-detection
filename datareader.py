import csv
import datetime
from typing import List

import numpy as np

from entities.tweet import Tweet
from my_utils.functions import ms_str
from my_utils.datareader import read_clustered
from my_utils.filters import threeshold_filter
from my_utils.datawriter import print_clustered

from structures.unionfind import UnionFind


cluster_filter_threshold: int = 100
clusters, cluster_counts, cluster_timestamps, tweets = read_clustered("data/1day/clusters.sortedby.clusterid.csv", True)

timestamps:np.array = np.array(cluster_timestamps)

f_clusters, f_cluster_centroids, f_cluster_entities = threeshold_filter(clusters, cluster_counts, timestamps, cluster_filter_threshold);

f_cluster_centroids = np.array(f_cluster_centroids)
centroids_sortedby_time = f_cluster_centroids[f_cluster_centroids[:, 1].argsort()]

# find similar clusters:
candidate_similar_clusters: dict = {}
window_timedelta = datetime.timedelta(hours=2)
window_timespan = window_timedelta.total_seconds() * 1000

# o(n^2) algorithm, needs improvement
for centroid in centroids_sortedby_time:
    cluster_id = centroid[0]
    window_start = centroid[1] - window_timespan
    window_end = centroid[1]
    for centroid_ in centroids_sortedby_time: # search again from the begining
        other_cluster_id = centroid_[0]

        if cluster_id not in candidate_similar_clusters:
            candidate_similar_clusters[cluster_id] = []

        if window_start >= centroid_[1] or centroid_[1] > window_end or cluster_id == other_cluster_id:
            continue # skip if its outside our time window

        overlap = f_cluster_entities[cluster_id].intersection(f_cluster_entities[other_cluster_id])
        if len(overlap) > 0: # if there is overlap,
            candidate_similar_clusters[cluster_id].append(other_cluster_id)

cluster_map: List = []

for cluster_id in candidate_similar_clusters:
    cluster_map.append(cluster_id)

uf = UnionFind(len(cluster_map))

superclusters: dict = { }

for i,original_cluster in enumerate(cluster_map):
    superclusters[i] = f_cluster_entities[original_cluster]
    for candidate in candidate_similar_clusters[original_cluster]:
        if uf.find(i, cluster_map.index(candidate)):
            continue
        uf.union(i, cluster_map.index(candidate))
        superclusters[i] = superclusters[i] | f_cluster_entities[candidate]

# for index, actual in enumerate(uf._id):
#     print(clusters[cluster_map[index]], superclusters[actual], index, "->", actual)

# now, filter tweets
new_selected_tweets: List[Tweet] = []
for t in tweets:
    real_cluster_id = t.cluster_id
    if real_cluster_id in f_clusters:
        mapped_cluster_id = cluster_map.index(real_cluster_id)
        t.cluster_id = real_cluster_id  # set new cluster
        t.cluster_name_entity = " ".join(superclusters[mapped_cluster_id])
        new_selected_tweets.append(t)
print("Original amount of tweets:", len(tweets), "\n",
      "New amount of tweets\t\t", len(new_selected_tweets))

print_clustered("my_results.csv", new_selected_tweets)

