#This code was modified from : https://www.learnpythonwithrune.org/how-to-plot-locations-of-tweets-on-map-using-python-in-3-easy-steps/
# Textblob analysis : https://medium.com/red-buffer/sentiment-analysis-let-textblob-do-all-the-work-9927d803d137#:~:text=When%20calculating%20a%20sentiment%20for,combined%20polarity%20for%20longer%20texts.

import tweepy
import folium
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from textblob import TextBlob
import re

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

    def getRawTweets(self, search_keyword, num_tweets):
        api = self.getTwitterApi()
        return tweepy.Cursor(api.search_tweets, q=search_keyword).items(num_tweets)

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def getCleanTweets(self, search_keyword, num_tweets):
        tweets = self.getRawTweets(search_keyword, num_tweets)
        for tweet in tweets:
            analysis = TextBlob(self.clean_tweet(tweet.text))
            #print(analysis.sentiment.polarity)


    def getTweets(self, search_keyword, num_tweets):
        location_data_array = []
        tweets = self.getRawTweets(search_keyword, num_tweets)

        for tweet in tweets:
                location_data = self.getTweetLocation(tweet)
                if len(location_data):
                    analysis = TextBlob(self.clean_tweet(tweet.text))
                    (location_data_array.append(location_data + (self.clean_tweet(tweet.text),) + (analysis.sentiment.polarity,)) if location_data is not None else None)

        return location_data_array

    def getTweetLocation(self, tweet):

        location_data = []

        if hasattr(tweet, 'user') and hasattr(tweet.user, 'screen_name') and hasattr(tweet.user, 'location'):
            if tweet.user.location:
                #location_data.append((tweet.user.screen_name, tweet.user.location))
                location_data = (tweet.user.screen_name, tweet.user.location)

        return location_data
