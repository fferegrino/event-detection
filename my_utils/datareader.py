import csv
from typing import Dict, List, Tuple, Set

import numpy as np
from entities.tweet import Tweet


def read_clustered(file: str, return_tweets: bool = False) \
        -> Tuple[Dict[int, Set[str]], Dict[int, int], np.array, List[Tweet]]:
    """
    Reads a csv file containing data from clustered tweets and return some useful arrays to work with them
    :param str file: The input file
    :param bool return_tweets: If True, this function will read and return tweets from te file
    :return:
        A tuple containing
        1) a dictionary where the keys are the Clusters Id and the values are sets with the entities of each cluster
        2) a dictionary where the keys are the Clusters Id an the values are the number of tweets in each cluster
        3) a np.array  where each row is a tweet and the columns are the columns are cluster_id, timestamp and user_id
        4) a list of tweets contained in the file
    :rtype: (dict, dict, np.array, list)
    """
    clusters: Dict[int, Set[str]] = {}
    intermediate_cluster_count: Dict[int, int] = {}
    intermediate_tweet_numbers: List[List[int]] = []
    tweets = []

    with open(file, 'r', encoding='utf-8') as reddit_posts_csv:
        reader = csv.reader(reddit_posts_csv, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            cluster_id = int(row[0])  # cluster id
            cluster_entity = row[1]  # cluster_name_entity
            timestamp_ms = int(row[3])  # timestamp_ms

            if return_tweets:
                t = Tweet(int(row[2]),  # tweet_id
                          timestamp_ms,
                          int(row[4]),  # user_id
                          row[6])  # tweet_text
                t.cluster_id = cluster_id
                t.tweet_tokens = row[5]  # tweet_tokens
                t.cluster_name_entity = cluster_entity
                tweets.append(t)

            intermediate_tweet_numbers.append([cluster_id, timestamp_ms, t.user_id])

            named_entities = set(cluster_entity.split(' '))
            if '' in named_entities:
                named_entities.remove('')

            if cluster_id not in clusters:
                clusters[cluster_id] = named_entities
                intermediate_cluster_count[cluster_id] = 0
            intermediate_cluster_count[cluster_id] = intermediate_cluster_count[cluster_id] + 1

    return (clusters,
            intermediate_cluster_count,
            np.array(intermediate_tweet_numbers),
            tweets)
