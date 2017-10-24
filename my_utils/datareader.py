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

            if cluster_id not in clusters:
                clusters[cluster_id] = cluster_entity
                intermediate_cluster_count[cluster_id] = 0
            intermediate_cluster_count[cluster_id] = intermediate_cluster_count[cluster_id] + 1

    return (clusters,
            intermediate_cluster_count,
            intermediate_tweet_numbers,
            tweets)
