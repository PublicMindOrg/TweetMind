#This code was modified from : https://www.learnpythonwithrune.org/how-to-plot-locations-of-tweets-on-map-using-python-in-3-easy-steps/

import tweepy
import folium
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim

class TwitterHelper:
    def __init__(self):
        self.consumer_key = "xbT3Y6EY0ysBxNa2ac4HzJCwi"
        self.consumer_secret = "fp7WMfnOIajMg4AXtsDluBVP7pdv0dj8hsFk3AchWE8MFgh5s3"
        self.access_token = "1516886677813436423-anLmErVObkOYBcpqJrQA6WCRouxLRW"
        self.access_token_secret = "8FToCh5P08iiu2tOKPknOcsmrT35hs0da8527nEBPI71d"

    def getTwitterApi(self):
        # authentication of consumer key and secret
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        # authentication of access token and secret
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        return api

    def getTweets(self, search_keyword, num_tweets):
        api = self.getTwitterApi()
        location_data_array = []

        tweets = tweepy.Cursor(api.search_tweets, q=search_keyword).items(num_tweets)

        for tweet in tweets:
                location_data = self.getTweetLocation(tweet)
                if len(location_data):
                    (location_data_array.append(location_data) if location_data is not None else None)

        return location_data_array

    def getTweetLocation(self, tweet):

        location_data = []

        if hasattr(tweet, 'user') and hasattr(tweet.user, 'screen_name') and hasattr(tweet.user, 'location'):
            if tweet.user.location:
                #location_data.append((tweet.user.screen_name, tweet.user.location))
                location_data = (tweet.user.screen_name, tweet.user.location)

        return location_data
