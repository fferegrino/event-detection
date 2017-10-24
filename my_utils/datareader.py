import csv

from entities.tweet import Tweet


def read_clustered(file: str, return_tweets: bool = False):
    """
    Reads a csv file containing data from clustered tweets and return some useful arrays to work with them
    :param file:
    :param return_tweets:
    :return:
    """
    clusters = {}
    intermediate_cluster_count = {}
    intermediate_tweet_numbers = []
    tweets = []

    with open(file, 'r', encoding='utf-8') as reddit_posts_csv:
        reader = csv.reader(reddit_posts_csv, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            cluster_id = int(row[0])
            cluster_entity = row[1]
            timestamp_ms = int(row[3])

            if return_tweets:
                t = Tweet(int(row[2]),
                          timestamp_ms,
                          int(row[4]),
                          row[6])
                t.cluster_id = cluster_id
                t.tweet_tokens = row[5]
                tweets.append(t)

            intermediate_tweet_numbers.append([cluster_id, timestamp_ms])

            if cluster_id not in clusters:
                clusters[cluster_id] = cluster_entity
                intermediate_cluster_count[cluster_id] = 0
            intermediate_cluster_count[cluster_id] = intermediate_cluster_count[cluster_id] + 1

    return (clusters,
            intermediate_cluster_count,
            intermediate_tweet_numbers,
            tweets)
