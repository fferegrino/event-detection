import csv
from typing import List

from entities.tweet import Tweet


def print_clustered(filename: str, tweets: List[Tweet]):
    """
    Writes the list of specified twetts to the specified file
    :param filename:
    :param tweets:
    :return:
    """
    with open(filename, 'w', encoding='utf8', newline='') as file:
        csv_writer = csv.writer(file, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for tweet in tweets:
            # TODO: Fix this ugly hack of the new lines
            tweet_text = tweet.tweet_text.replace('\n', ' ')
            csv_writer.writerow((tweet.cluster_id,
                                 tweet.cluster_name_entity,
                                 tweet.tweet_id,
                                 tweet.timestamp_ms,
                                 tweet.user_id,
                                 tweet.tweet_tokens,
                                 tweet_text))
