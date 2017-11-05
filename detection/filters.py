from typing import Dict, List, Tuple, Set

import numpy as np


def threshold_filter(cluster_counts: Dict[int, int], timestamps: np.array, cluster_filter_threshold: int) \
        -> Tuple[Set[int], np.array]:
    """
    Filters clusters that contain less than the int{cluster_filter_threshold} specified number of tweets.
    It also calculates the centroid times for each of the filtered.
    :param cluster_counts: a dictionary containing the number of tweets per cluster
    :param timestamps: an array containing the timestamps for each tweet
    :param cluster_filter_threshold: the number of tweets needed for a cluster to be considered relevant
    :return:
        A tuple containing
        1) a set containing the cluster id of the selected clusters
        3) a np.array containing the time centroids for each one of the selected clusters
    :rtype: (set, np.array)
    """
    filtered_clusters: Set[int] = set()
    relevant_cluster_centroids: List[List[int]] = []

    for c_id in cluster_counts:
        if cluster_counts[c_id] > cluster_filter_threshold:
            timestamp_centroid = int(np.mean(timestamps[timestamps[:, 0] == c_id][:, 1]))
            relevant_cluster_centroids.append([c_id, timestamp_centroid])
            filtered_clusters.add(c_id)

    return filtered_clusters, np.array(relevant_cluster_centroids)