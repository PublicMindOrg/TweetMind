import folium
from TwitterHelper import *
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim


def put_markers(map, data):
    geo_locator = Nominatim(user_agent="LearnPython")
    for (name, location, tweet_text, sentiment) in data:
        if location:
            try:
                location = geo_locator.geocode(location)
                if location:
                    if sentiment > 0: 
                        folium.Marker([location.latitude, location.longitude],  icon=folium.Icon(color='green'),  popup=tweet_text).add_to(map)
                    elif sentiment < 0:
                        folium.Marker([location.latitude, location.longitude],  icon=folium.Icon(color='red'),  popup=tweet_text).add_to(map)
                    else:
                        folium.Marker([location.latitude, location.longitude],  icon=folium.Icon(color='lightgray'),  popup=tweet_text).add_to(map)
            except GeocoderTimedOut:
                continue
            



if __name__ == "__main__":
    map = folium.Map(location=[0, 0], zoom_start=2)
    th = TwitterHelper()
    search_string = "#Ukraine"
    location_data = th.getTweets(search_string, 150)
    sentiment_data = th.getCleanTweets(search_string, 150)
    print(location_data)
    put_markers(map, location_data)
    map.save("index2.html")