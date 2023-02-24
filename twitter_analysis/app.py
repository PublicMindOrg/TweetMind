from flask import Flask, render_template
import os
from pymongo import MongoClient
import requests
import csv
from decouple import config
from datetime import datetime
import pickle
from xgboost import XGBClassifier
import numpy as np
from collections import deque
import pandas as pd 
from pandas import MultiIndex, Int16Dtype
import json
app = Flask(__name__)


class TweetCollection:
    def __init__(self):
        f = open('topics.json')
        self.query_list = deque(json.load(f))

    def get_tweets(self):
        while True:
            self.get_all_tweets()

    def get_all_tweets(self):
        query_params = ''
        TWITTER_API_1 = config('TWITTER_API_1')
        q_obj = self.query_list.popleft()
        if 'next_results' not in q_obj.keys():
            query_params = "?q="+q_obj['query']+" AND -filter:retweets&country_code=US&result_type=recent&count=100&lang=en&tweet_mode=extended"
        else:
            query_params = q_obj['next_results']
        headers = {'Authorization': config('API_TOKEN')}
        api_url = TWITTER_API_1 + query_params
        cluster= MongoClient(config('MONGO_URL'))
        db = cluster['TweetMind']
        collection = db['tweets_data']
        tweets = requests.get(api_url,headers=headers).json()
        if 'next_results' in tweets['search_metadata'].keys():
            param = tweets['search_metadata']['next_results']
            q_obj['next_results'] = param +'&tweet_mode=extended'
        self.query_list.append(q_obj)
        count = 0
        for i in tweets['statuses']:
            count+=1
            user= i['user']
            # print(datetime.now())
            # print(datetime.strptime(user['created_at'],'%a %b %d %X %z %Y').replace(tzinfo=None))
            account_age_days = (datetime.now() - datetime.strptime(user['created_at'],'%a %b %d %X %z %Y').replace(tzinfo=None)).days
            verified = user['verified']
            geo_enabled = user['geo_enabled']
            default_profile = user['default_profile']
            default_profile_image = user['default_profile_image']
            favourites_count = user['favourites_count']
            followers_count = user['followers_count']
            friends_count = user['friends_count']
            statuses_count = user['statuses_count']
            average_tweets_per_day = np.round(statuses_count / 1+account_age_days, 3)

            # manufactured features
            hour_created = int(datetime.strptime(user['created_at'],'%a %b %d %X %z %Y').replace(tzinfo=None).strftime('%H'))
            network = np.round(np.log(1 + friends_count)
                            * np.log(1 + followers_count), 3)
            tweet_to_followers = np.round(
                np.log(1 + statuses_count) * np.log(1 + followers_count), 3)
            follower_acq_rate = np.round(
                np.log(1 + (followers_count / 1+account_age_days)), 3)
            friends_acq_rate = np.round(
                np.log(1 + (friends_count / 1+account_age_days)), 3)

            # organizing list to be returned
            user_features = [verified, hour_created, geo_enabled, default_profile, default_profile_image,
                                favourites_count, followers_count, friends_count, statuses_count,
                                average_tweets_per_day, network, tweet_to_followers, follower_acq_rate,
                                friends_acq_rate]
            # features for model
            features = ['verified', 'hour_created', 'geo_enabled', 'default_profile', 'default_profile_image',
                        'favourites_count', 'followers_count', 'friends_count', 'statuses_count', 'average_tweets_per_day',
                        'network', 'tweet_to_followers', 'follower_acq_rate', 'friends_acq_rate']

            # creates df for model.predict() format
            user_df = pd.DataFrame(np.matrix(user_features), columns=features)
            xgb_model = self.load_pkl('model_file_name.json')
            prediction = xgb_model.predict(user_df)[0]
            f = open('bot_data.csv', 'a')
            writer = csv.writer(f)
            user_features.append(prediction)
            # write a row to the csv file
            writer.writerow(user_features)

            # close the file
            f.close()
            
            if prediction==0:
                print('Added')
                collection.insert_one({'tweet':i['full_text'],'language':i['lang'],'created_at':str(datetime.strptime(i['created_at'],'%a %b %d %X %z %Y').replace(tzinfo=None).date()),'topic':q_obj['topic'],'query':q_obj['query']})
            
        print('Number of tweets: '+str(count))
    
    def load_pkl(self,fname):
        model2 = XGBClassifier()
        model2.load_model(fname)
        return model2
    
    def clean_data(self):
        cluster = MongoClient(config('MONGO_URL'))
        db = cluster['TweetMind']
        collection = db['tweets_data']
        tweets = list(collection.find())
        s = set()
        cleant_arr = []
        print(len(tweets))
        for tweet in tweets:
            if tweet['tweet'] not in s:
                s.add(tweet['tweet'])
                cleant_arr.append(tweet)
        file = open("file1.txt", "w+")
        
        # Saving the array in a text file
        content = str(cleant_arr)
        file.write(content)
        file.close()
        print((cleant_arr[0]))
        collection.drop()
        for i in cleant_arr:
            collection.insert_one(i)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/getTweets')
def getTweets():
    twitobj = TweetCollection()
    twitobj.get_tweets()
    return 'Hi'

@app.route('/cleanTweets')
def cleanTweets():
    twitobj = TweetCollection()
    twitobj.clean_data()
    return 'Cleaning Done'

@app.route('/convertData')
def convertData():
    cluster = MongoClient(config('MONGO_URL'))
    db = cluster['TweetMind']
    collection = db['tweets_data']
    topics = ['Academic Workers Strike','Climate Change','Russia Ukraine War','Layoffs','Gun Violence']
    for i in topics:
        headers = ['Id','Tweet','Language','Created At','Topic','Query']
        tweets = list(collection.find({'topic':i}))
        f = open('./folder_1/'+i+'.csv', 'w+')
        writer = csv.writer(f)
        # write a row to the csv file
        writer.writerow(headers)
        for tweet in tweets:
            writer.writerow([tweet['_id'],tweet['tweet'],tweet['language'],tweet['created_at'],tweet['topic'],tweet['query']])
        f.close()
    return 'Converted'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run()