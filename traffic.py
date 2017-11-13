from typing import Set

from nltk.tokenize import word_tokenize

from inputoutput.datareader import read_clustered
from structures.tweet import Tweet

# get the traffic words:
with open('traffic_words.txt') as f:
    content = f.readlines()
traffic_words: Set[str] = set([x.strip() for x in content])

# Read only the tweets!
_,_,_,t = read_clustered('data/1day/clusters.sortedby.clusterid.csv', True)

# retokenize tweets:
a = 0
for tweet in t:
    tweet : Tweet = tweet
    words = word_tokenize(tweet.tweet_text)
    for w in words:
        if w in traffic_words:
            a = a + 1

print(a)