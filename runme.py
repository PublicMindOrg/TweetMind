import folium
from TwitterHelper import *
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim


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
    th = TwitterHelper()
    search_string = "#100DaysOfCode"
    location_data = th.getTweets(search_string, 150)
    print(location_data)
    put_markers(map, location_data)
    map.save("index2.html")