#This code was taken from : https://www.learnpythonwithrune.org/how-to-plot-locations-of-tweets-on-map-using-python-in-3-easy-steps/

import tweepy
import folium
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim

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

def get_tweets(search):
    api = get_twitter_api()
    location_data = []

    for tweet in tweepy.Cursor(api.search_tweets, q=search).items(500):
        if hasattr(tweet, 'user') and hasattr(tweet.user, 'screen_name') and hasattr(tweet.user, 'location'):
            if tweet.user.location:
                location_data.append((tweet.user.screen_name, tweet.user.location))
    return location_data

def put_markers(map, data):
    geo_locator = Nominatim(user_agent="LearnPython")
    for (name, location) in data:
        if location:
            try:
                location = geo_locator.geocode(location)
            except GeocoderTimedOut:
                continue
            if location:
                folium.Marker([location.latitude, location.longitude], popup=name).add_to(map)

if __name__ == "__main__":
    map = folium.Map(location=[0, 0], zoom_start=2)
    location_data = get_tweets("#100DaysOfCode")
    put_markers(map, location_data)
    map.save("index.html")