class Tweet:
    def __init__(self, tweet_id, timestamp_ms, user_id, tweet_text):
        self.tweet_id = tweet_id
        self.timestamp_ms = timestamp_ms
        self.user_id = user_id
        self.tweet_text = tweet_text

        self.cluster_id = None
        self.cluster_name_entity = None
        self.tweet_tokens = None