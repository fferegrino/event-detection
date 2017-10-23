import csv
import datetime
import numpy as np

from entities.tweet import Tweet
from my_utils.functions import ms_str
from my_utils.datareader import read_clustered
from my_utils.filters import threeshold_filter

from structures.unionfind import UnionFind


cluster_filter_threshold = 300

clusters, cluster_counts, cluster_timestamps, tweets = read_clustered("data/7days/clusters.sortedby.clusterid.csv")

timestamps = np.array(cluster_timestamps)

f_clusters, f_cluster_centroids, f_cluster_entities = threeshold_filter(clusters, cluster_counts, timestamps, cluster_filter_threshold);

f_cluster_centroids = np.array(f_cluster_centroids)
centroids_sortedby_time = f_cluster_centroids[f_cluster_centroids[:, 1].argsort()]

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

        overlap = f_cluster_entities[cluster_id].intersection(f_cluster_entities[other_cluster_id])
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