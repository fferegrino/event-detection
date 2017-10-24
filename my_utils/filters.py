import numpy as np


def threeshold_filter(clusters: dict, cluster_counts: dict, timestamps: np.array, cluster_filter_threshold: int):
    # filter out small clusters & centroid calculation
    filtered_clusters = set()
    relevant_cluster_centroids = []
    cluster_entities = {}

    for c_id in clusters:
        if cluster_counts[c_id] > cluster_filter_threshold:
            timestamp_centroid = int(np.mean(timestamps[timestamps[:, 0] == c_id][:, 1]))

            filtered_clusters.add(c_id)
            cluster_entities[c_id] = set(clusters[c_id].split(' '))
            if '' in cluster_entities[c_id]:
                cluster_entities[c_id].remove('')
            relevant_cluster_centroids.append([c_id, timestamp_centroid])

    return filtered_clusters, relevant_cluster_centroids, cluster_entities
