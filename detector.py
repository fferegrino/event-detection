import argparse
import datetime
from typing import List, Dict

import numpy as np

from entities.tweet import Tweet
from my_utils.functions import ms_str
from my_utils.grouping import find_similar
from my_utils.datareader import read_clustered
from my_utils.datawriter import print_clustered
from my_utils.filters import threeshold_filter, threeshold_horoscope_filter
from structures.unionfind import UnionFind

parser = argparse.ArgumentParser(description='Do some cluster magic!')
parser.add_argument('threshold', metavar='sub', type=int,
                    help='the minimum amount of tweets per cluster')
parser.add_argument("data_file", action="store",
                    help="the file containing the clusters")
parser.add_argument("-o", "--output_file", action="store",
                    help="the file where I should save the results")
parser.add_argument("-v", "--verbose", help="should i tell you everything im doing?",
                    action="store", default=True)


def main(args=None):
    """The main routine."""

    args = parser.parse_args()
    cluster_filter_threshold = args.threshold
    data_file = args.data_file

    output_file = args.output_file
    if output_file is None:
        output_file = "results-" + str(cluster_filter_threshold) + ".csv"

    clusters, cluster_counts, cluster_timestamps, tweets = read_clustered(data_file, True)

    timestamps: np.array = np.array(cluster_timestamps)

    f_clusters, f_cluster_centroids, f_cluster_entities = threeshold_horoscope_filter(clusters, cluster_counts, timestamps,
                                                                            cluster_filter_threshold);

    f_cluster_centroids = np.array(f_cluster_centroids)

    # find similar clusters:
    window_timedelta = datetime.timedelta(hours=2)
    candidate_similar_clusters: dict = find_similar(f_cluster_centroids, f_cluster_centroids, window_timedelta)

    cluster_map: List = []

    for cluster_id in candidate_similar_clusters:
        cluster_map.append(cluster_id)

    uf = UnionFind(len(cluster_map))

    superclusters: dict = {}

    for i, original_cluster in enumerate(cluster_map):
        superclusters[i] = f_cluster_entities[original_cluster]
        for candidate in candidate_similar_clusters[original_cluster]:
            if uf.find(i, cluster_map.index(candidate)):
                continue
            uf.union(i, cluster_map.index(candidate))
            superclusters[i] = superclusters[i] | f_cluster_entities[candidate]

    # now, filter tweets
    new_selected_tweets: List[Tweet] = []
    for t in tweets:
        real_cluster_id = t.cluster_id
        if real_cluster_id in f_clusters:
            mapped_cluster_id = cluster_map.index(real_cluster_id)
            t.cluster_id = real_cluster_id  # set new cluster
            t.cluster_name_entity = " ".join(superclusters[mapped_cluster_id])
            new_selected_tweets.append(t)

    if args.verbose:
        print("Original amount of tweets:\t", len(tweets))
        print("New amount of tweets:\t\t", len(new_selected_tweets))

    print_clustered(output_file, new_selected_tweets)


if __name__ == "__main__":
    main()
