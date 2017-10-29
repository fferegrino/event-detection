from typing import Dict, List

import numpy as np


def threeshold_filter(clusters: Dict[int, str], cluster_counts: Dict[int, int], timestamps: np.array,
                      cluster_filter_threshold: int):
    # filter out small clusters & centroid calculation
    filtered_clusters: set = set()
    relevant_cluster_centroids: List[List[int]] = []
    cluster_entities = {}

    for c_id in clusters:
        if cluster_counts[c_id] > cluster_filter_threshold:
            named_entities = set(clusters[c_id].split(' '))
            if '' in named_entities:
                named_entities.remove('')

            timestamp_centroid = int(np.mean(timestamps[timestamps[:, 0] == c_id][:, 1]))
            filtered_clusters.add(c_id)
            cluster_entities[c_id] = named_entities
            relevant_cluster_centroids.append([c_id, timestamp_centroid])

    return filtered_clusters, np.array(relevant_cluster_centroids), cluster_entities


horoscope_words = {'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius',
                   'capricorn', 'aquarius', 'pisces'}


def threeshold_horoscope_filter(clusters: Dict[int, str], cluster_counts: Dict[int, int], timestamps: np.array,
                                cluster_filter_threshold: int):
    # filter out small clusters & centroid calculation
    filtered_clusters: set = set()
    relevant_cluster_centroids: List[List[int]] = []
    cluster_entities = {}

    for c_id in clusters:
        if cluster_counts[c_id] > cluster_filter_threshold:
            named_entities = set(clusters[c_id].split(' '))

            # check for horoscope words, if found, skip filter this cluster out
            if len(named_entities) == 1 and len(named_entities.intersection(horoscope_words)) > 0:
                continue

            if '' in named_entities:
                named_entities.remove('')

            timestamp_centroid = int(np.mean(timestamps[timestamps[:, 0] == c_id][:, 1]))
            filtered_clusters.add(c_id)
            cluster_entities[c_id] = named_entities
            relevant_cluster_centroids.append([c_id, timestamp_centroid])

    return filtered_clusters,  np.array(relevant_cluster_centroids), cluster_entities
