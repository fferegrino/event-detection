import csv
from typing import List

from entities.tweet import Tweet


def print_clustered(filename: str, tweets: List[Tweet]):
    with open(filename, 'w', encoding='utf-8') as reddit_posts_csv:
        submwriter = csv.writer(reddit_posts_csv, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for tweet in tweets:
            # TODO: Fix this ugly hack of the new lines
            tweet_text = tweet.tweet_text.replace('\n', ' ')
            submwriter.writerow((tweet.cluster_id,
                                 tweet.cluster_name_entity,
                                 tweet.tweet_id,
                                 tweet.timestamp_ms,
                                 tweet.user_id,
                                 tweet.tweet_tokens,
                                 tweet_text))
