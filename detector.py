import argparse
import datetime
from typing import List, Dict

import numpy as np

from entities.tweet import Tweet
from entities.burst import Burst
from my_utils.functions import ms_str
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
    if output_file == None:
        output_file = "results-" + str(cluster_filter_threshold) + ".csv"

    clusters, cluster_counts, cluster_timestamps, tweets = read_clustered(data_file, True)

    timestamps: np.array = np.array(cluster_timestamps)

    # by_user_counts: Dict[int, int] = {}
    #
    # for row in range(len(timestamps)):
    #     user_id = timestamps[row][2]
    #     if user_id not in by_user_counts:
    #         by_user_counts[user_id] = 0
    #     by_user_counts[user_id] = by_user_counts[user_id] + 1
    #
    # for uid in by_user_counts:
    #     if by_user_counts[uid] > 20:
    #         print(uid)
    #         for t in tweets:
    #             if t.user_id == uid:
    #                 print(ms_str(t.timestamp_ms), t.cluster_name_entity, t.tweet_text)
    #
    # return

    burst_time = 60000 * 1
    burst_size = 15

    possible_brusts:Dict[str, Burst] = {}

    for t in tweets[:10000]:
        topics = t.cluster_name_entity.split(' ')
        for topic in topics:
            if topic not in possible_brusts:
                possible_brusts[topic] = Burst(topic)
            current_burst: Burst = possible_brusts[topic]
            current_burst.add_document(t)

        current_timestamp = t.timestamp_ms
        # Clean past brusts:
        bursts_to_delete = []
        bursts_to_save = []
        for br in possible_brusts:
            burst = possible_brusts[br]
            if burst.max_date() < current_timestamp - burst_time and len(burst) < burst_size:
                #print("To delete", burst.entity)
                bursts_to_delete.append(br)
            elif burst.max_date() < current_timestamp - burst_time and len(burst) >= burst_size:
                #print("To save", burst.entity)
                bursts_to_save.append(br)


        for to_delete in bursts_to_delete:
            del possible_brusts[to_delete]
        for to_save in bursts_to_save:
            del possible_brusts[to_save]

    for p in possible_brusts:
        burst = possible_brusts[p]
        print(burst.entity, len(burst), ms_str(burst.min_date()), ms_str(burst.max_date()))

    print("Bursts:", len(possible_brusts))

    #for b in possible_brusts:
    #    burst = possible_brusts[b]
    #    print(burst.entity, burst.size(), ms_str( burst.min_document_date()) , ms_str( burst.max_document_date()))

    return


    f_clusters, f_cluster_centroids, f_cluster_entities = threeshold_horoscope_filter(clusters, cluster_counts, timestamps,
                                                                            cluster_filter_threshold);

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
        for centroid_ in centroids_sortedby_time:  # search again from the begining
            other_cluster_id = centroid_[0]

            if cluster_id not in candidate_similar_clusters:
                candidate_similar_clusters[cluster_id] = []

            if window_start >= centroid_[1] or centroid_[1] > window_end or cluster_id == other_cluster_id:
                continue  # skip if its outside our time window

            overlap = f_cluster_entities[cluster_id].intersection(f_cluster_entities[other_cluster_id])
            if len(overlap) > 0:  # if there is overlap,
                candidate_similar_clusters[cluster_id].append(other_cluster_id)

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
