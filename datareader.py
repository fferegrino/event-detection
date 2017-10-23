import csv
import datetime
import numpy as np

from entities.tweet import Tweet
from my_utils.functions import ms_str
from my_utils.datareader import read_clustered

from structures.unionfind import UnionFind


cluster_filter_threshold = 100

clusters, intermediate_cluster_count, intermediate_tweet_numbers, tweets = read_clustered("data/7days/clusters.sortedby.clusterid.csv")

tweet_numbers = np.array(intermediate_tweet_numbers)

# filter out small clusters & centroid calculation
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

        overlap = cluster_entities[cluster_id].intersection(cluster_entities[other_cluster_id])
        if len(overlap) > 0: # if there is overlap,
            candidate_similar_clusters[cluster_id].append(other_cluster_id)

cluster_remap = []

for cluster_id in candidate_similar_clusters:
    cluster_remap.append(cluster_id)

uf = UnionFind(len(cluster_remap))

for i,original_cluster in enumerate(cluster_remap):
    for candidate in candidate_similar_clusters[original_cluster]:
        if uf.find(i, cluster_remap.index(candidate)):
            print("Already joined!")
            continue
        uf.union(i, cluster_remap.index(candidate))


for i, c_id in enumerate(uf._id):
    i_mapped = cluster_remap[i]
    cid_mapped = cluster_remap[c_id]
    if i_mapped != cid_mapped:
        print(clusters[i_mapped],"merged with", clusters[cid_mapped])