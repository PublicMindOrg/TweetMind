import tweepy

def get_twitter_api():
    # personal details
    consumer_key = "xbT3Y6EY0ysBxNa2ac4HzJCwi"
    consumer_secret = "fp7WMfnOIajMg4AXtsDluBVP7pdv0dj8hsFk3AchWE8MFgh5s3"
    access_token = "1516886677813436423-anLmErVObkOYBcpqJrQA6WCRouxLRW"
    access_token_secret = "8FToCh5P08iiu2tOKPknOcsmrT35hs0da8527nEBPI71d"
    # authentication of consumer key and secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # authentication of access token and secret
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

def get_twitter_location(search):
    api = get_twitter_api()
    count = 0

    for tweet in tweepy.Cursor(api.search_tweets, q=search).items(500):
        if hasattr(tweet, 'coordinates') and tweet.coordinates is not None:
            count += 1
            print("Coordinates", tweet.coordinates)
        if hasattr(tweet, 'location') and tweet.location is not None:
            count += 1
            print("Coordinates", tweet.location)
    print(count)

get_twitter_location("#100DaysOfCode")