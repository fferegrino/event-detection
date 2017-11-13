from typing import Set, Dict, List, Tuple

import numpy as np

from structures.unionfind import UnionFind

def find_similar_clusters(entities: Dict[int, Set[str]], centroids: np.array,
                          delta: int) -> Dict[int, List[int]]:
    """
    Naively finds similar clusters based on a certain time window
    :param entities: a dictionary containing the sets of entities for each cluster
    :param centroids: an array of the time centroids
    :param delta: the time window to take into account
    :return: a dictionary containing lists of possible candidate similar clusters
    """
    candidate_similar_clusters: Dict[int, List[int]] = {}
    centroids_sortedby_time = centroids[centroids[:, 1].argsort()]

    window_timespan = delta * 1000

    # o(n^2) algorithm, needs improvement
    for centroid in centroids_sortedby_time:
        cluster_id = centroid[0]
        window_start = centroid[1] - window_timespan
        window_end = centroid[1]
        for centroid_ in centroids_sortedby_time:  # search again from the begining
            other_id = centroid_[0]
            if cluster_id not in candidate_similar_clusters:
                candidate_similar_clusters[cluster_id] = []
            if cluster_id == other_id:
                continue
            if window_start <= centroid_[1] < window_end:
                overlap = entities[cluster_id].intersection(entities[other_id])
                if len(overlap) > 0:  # if there is overlap,
                    candidate_similar_clusters[cluster_id].append(other_id)

    return candidate_similar_clusters


def join_superclusters(entities: Dict[int, Set[str]], candidate_similar_clusters: Dict[int, List[int]]) \
        -> Tuple[UnionFind, List[int], Dict[int, Set[str]]]:
    """
    Merge candidate similar clusters using a union-find data structure
    :param entities: a dictionary containing the sets of entities for each cluster
    :param candidate_similar_clusters: a dictionary containing lists of possible candidate similar clusters
    :return:
        A tuple containing
        1) the union-find structure used to merge the clusters
        2) a list containing the original cluster id, this list serves as a map between the original ids and the union-find id
        3) a dictionary containing the sets of merged entities for each supercluster
    :rtype: (list, dict)
    """
    cluster_map: List[int] = []

    for cluster_id in candidate_similar_clusters:
        cluster_map.append(cluster_id)

    uf = UnionFind(len(cluster_map))
    superclusters: Dict[int, Set[str]] = {}

    for i, original_cluster in enumerate(cluster_map):
        superclusters[i] = entities[original_cluster]
        for candidate in candidate_similar_clusters[original_cluster]:
            if uf.find(i, cluster_map.index(candidate)):
                continue
            uf.union(i, cluster_map.index(candidate))
            superclusters[i] = superclusters[i] | entities[candidate]

    return (uf, cluster_map, superclusters)
