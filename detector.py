import argparse
import numpy as np
from typing import List

from detection.filters import threshold_filter
from detection.grouping import find_similar_clusters, join_superclusters
from inputandoutput.datareader import read_clustered
from inputandoutput.datawriter import print_clustered
from structures.tweet import Tweet
from utils.functions import ms_str

parser = argparse.ArgumentParser(description='Do some cluster magic!')
parser.add_argument('threshold', metavar='sub', type=int,
                    help='the minimum amount of tweets per cluster')
parser.add_argument('window_seconds', metavar='sub', type=int,
                    help='time frame to consdider when merging clusters')
parser.add_argument("data_file", action="store",
                    help="the file containing the clusters")
parser.add_argument("-o", "--output_file", action="store",
                    help="the file where I should save the results")
parser.add_argument("-v", "--verbose", help="should i tell you everything im doing?",
                    action="store", default=True)


def main(args=None):
    args = parser.parse_args()
    cluster_filter_threshold = args.threshold
    data_file = args.data_file
    output_file = args.output_file
    if output_file is None:
        output_file = "results-" + str(cluster_filter_threshold) + ".csv"

    cluster_entities, cluster_counts, timestamps, tweets = read_clustered(data_file, True)

    windows = 24
    window_timeframes = 5

    min_time = tweets[0].timestamp_ms
    max_time = tweets[-1].timestamp_ms

    time_stops = [int(time) for time in np.linspace(min_time, max_time, windows+1)][1:]
    current_stop = 0
    for t in Tweet
    print("Earliest", ms_str(min_time))
    print("Latest  ", ms_str(max_time))
    for tim in time_stops:
        print(ms_str(tim))

    return

    filtered_clusters, time_centroids = threshold_filter(cluster_counts, timestamps, cluster_filter_threshold)

    candidate_similar_clusters: dict = find_similar_clusters(cluster_entities, time_centroids, args.window_seconds)

    uf, cluster_map, superclusters = join_superclusters(cluster_entities, candidate_similar_clusters)

    # now, filter tweets
    new_selected_tweets: List[Tweet] = []
    for t in tweets:
        real_cluster_id = t.cluster_id
        if real_cluster_id in filtered_clusters:
            mapped_cluster_id = cluster_map.index(real_cluster_id)
            t.cluster_id = uf._root(mapped_cluster_id)  # set new cluster
            t.cluster_name_entity = " ".join(superclusters[mapped_cluster_id])

            new_selected_tweets.append(t)

    if args.verbose:
        print("Original amount of tweets:\t", len(tweets))
        print("New amount of tweets:\t\t", len(new_selected_tweets))

    print_clustered(output_file, new_selected_tweets)


if __name__ == "__main__":
    main()
