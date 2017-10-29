import datetime
from typing import Set, Dict, List

import numpy as np


def find_similar(cluster_entities: Dict[int, Set[str]],
                 cluster_centroids: np.array,
                 time_delta: datetime.timedelta):
    candidate_similar_clusters: Dict[int, List[int]] = {}
    centroids_sortedby_time = cluster_centroids[cluster_centroids[:, 1].argsort()]

    window_timespan = time_delta.total_seconds() * 1000

    # o(n^2) algorithm, needs improvement
    for centroid in centroids_sortedby_time:
        cluster_id = centroid[0]
        window_start = centroid[1] - window_timespan
        window_end = centroid[1]
        for centroid_ in centroids_sortedby_time:  # search again from the begining
            other_cluster_id = centroid_[0]

            if cluster_id not in candidate_similar_clusters:
                candidate_similar_clusters[cluster_id] = []

            if window_start >= centroid_[1] or centroid_[1] > window_end or cluster_id == other_cluster_id:
                continue  # skip if its outside our time window

            overlap = cluster_entities[cluster_id].intersection(cluster_entities[other_cluster_id])
            if len(overlap) > 0:  # if there is overlap,
                candidate_similar_clusters[cluster_id].append(other_cluster_id)

    return candidate_similar_clusters
