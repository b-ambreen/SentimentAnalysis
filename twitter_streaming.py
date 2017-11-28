try:
    import json
except ImportError:
    import simplejson as json

from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

ACCESS_TOKEN = '85316100-caUJSUBLoUPbvNPBOiBujlR0JCR4sthRQof7o1DUQ'
ACCESS_SECRET = 'sO0MyNS8fMI5vMtHWIvNxcEbaVsqEfYO3GQlJMloapxae'
CONSUMER_KEY = 'QidFaO7O9iKLosUZdWRdHzcBj'
CONSUMER_SECRET = 'gmRDnj286qSWd55efgmwFbaVxoTdvio5OhJt25NZz7WwAvnJmo'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)


twitter_stream = TwitterStream(auth=oauth)

iterator = twitter_stream.statuses.sample()

tweet_count = 10000
for tweet in iterator:
    tweet_count -= 1
    
    print (json.dumps(tweet))  
    
    if tweet_count <= 0:
        break 
