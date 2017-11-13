from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import json

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key=""
consumer_secret=""

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="-"
access_token_secret=""

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        tweet = json.loads(data)
        with open("traffic/official/" + str(tweet["id"]) +".json", "w") as f:
            f.write(data)
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)


    stream.filter(track=['Isidrocorro',
                            'Peaton_No',
                            'ApoyoVial',
                            'AA_DF',
                            'OVIALCDMX',
                            '072AvialCDMX',
                            'GobCDMX',
                            'UCS_CDMX'])