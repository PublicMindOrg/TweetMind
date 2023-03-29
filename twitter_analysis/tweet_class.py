from pymongo import MongoClient
from decouple import config
from xgboost import XGBClassifier
from datetime import datetime
from collections import deque
import numpy as np
import math
import csv
import requests
import json
import pandas as pd 

# This class has all the functionalities used for the pipeline like:
# 1. Creating a Database Connection
# 2. Calling Twitter API
# 3. Getting User Features 
# 4. Adding a Bot Detector 
# 5. Storing the data in MongoDB
# 6. Deduplication of the data in MongoDB 
class TweetCollection:
    def __init__(self):
        try:
            topic_file = open('topics.json')
            self.query_list = deque(json.load(topic_file))
        except FileNotFoundError as e:
            print("File not found: ",e)

    def convert_date(self,date):
        if '/' in date:
            date = date.split('/')
            return date[2]+'-'+date[1]+'-'+date[0]
        return date
    
    def get_topic_data(self):
        graph_data = {}
        collection = self.get_db_connection('results_data')
        topic_list = ['Academic Workers Strike','Climate Change','Russia Ukraine War','Layoffs','Gun Violence']
        for topic in topic_list:
            tweets = list(collection.find({'Topic':topic}))
            list_collection = list(tweets)
            df = pd.DataFrame(list_collection)
            df['Created At'] = df['Created At'].apply(self.convert_date)
            grouped = df.groupby(by='Created At')['predicted'].value_counts()
            unstacked = grouped.unstack(level=1)

            udict = unstacked.to_dict('index')
            x_list = []
            y_list = []
            for key, val in udict.items():
                x_list.append(key)
                v1 = [v for v in val.values()]
                y_list.append(v1)

            neg_list = [0 if math.isnan(x[0]) else x[0] for x in y_list]
            neu_list = [0 if math.isnan(x[1]) else x[1] for x in y_list]
            pos_list = [0 if math.isnan(x[2]) else x[2] for x in y_list]
            
            graph_data[topic] = {
    
                'X_data':x_list,
                'Y_data':{
                  'Negative':neg_list,
                  'Positive':pos_list,
                  'Neutral':neu_list
                  }
            }
        return graph_data

    def get_db_connection(self,collection_name):
        try:
            cluster = MongoClient(config('MONGO_URL'))
            db = cluster['TweetMind']
            collection = db[collection_name]
            return collection
        except Exception as e:
            print('Failure occured \n Reason :',e)

    def get_tweets(self):
        while True:
            self.get_all_tweets()

    def get_user_features(self,user_data):
        account_age_days = (datetime.now() - datetime.strptime(user_data['created_at'],'%a %b %d %X %z %Y').replace(tzinfo=None)).days
        verified = user_data['verified']
        geo_enabled = user_data['geo_enabled']
        default_profile = user_data['default_profile']
        default_profile_image = user_data['default_profile_image']
        favourites_count = user_data['favourites_count']
        followers_count = user_data['followers_count']
        friends_count = user_data['friends_count']
        statuses_count = user_data['statuses_count']
        average_tweets_per_day = np.round(statuses_count / 1+account_age_days, 3)

        # manufactured features
        hour_created = int(datetime.strptime(user_data['created_at'],'%a %b %d %X %z %Y').replace(tzinfo=None).strftime('%H'))
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
        return user_features

    def get_all_tweets(self):
        try:
            query_params = ''
            TWITTER_API_1 = config('TWITTER_API_1')
            if len(self.query_list):
                q_obj = self.query_list.popleft()
                if 'next_results' not in q_obj.keys():
                    query_params = "?q="+q_obj['query']+" AND -filter:retweets&country_code=US&result_type=recent&count=100&lang=en&tweet_mode=extended"
                else:
                    query_params = q_obj['next_results']
                headers = {'Authorization': config('API_TOKEN')}
                api_url = TWITTER_API_1 + query_params
                collection = self.get_db_connection('tweets_data')
                tweets = requests.get(api_url,headers=headers).json()
                if tweets['search_metadata'] and 'next_results' in tweets['search_metadata'].keys():
                    param = tweets['search_metadata']['next_results']
                    q_obj['next_results'] = param +'&tweet_mode=extended'
                self.query_list.append(q_obj)
                count = 0
                for tweet in tweets['statuses']:
                    count+=1
                    user_data= tweet['user']
                    user_features = self.get_user_features(user_data)
                    # features for model
                    features = ['verified', 'hour_created', 'geo_enabled', 'default_profile', 'default_profile_image',
                                'favourites_count', 'followers_count', 'friends_count', 'statuses_count', 'average_tweets_per_day',
                                'network', 'tweet_to_followers', 'follower_acq_rate', 'friends_acq_rate']

                    # creates df for model.predict() format
                    user_df = pd.DataFrame(np.matrix(user_features), columns=features)
                    try:
                        xgb_model = self.load_bot_model('model_file_name.json')
                        prediction = xgb_model.predict(user_df)[0]
                        bot_file = open('./folder_1/bot_data.csv', 'a')
                        writer = csv.writer(bot_file)
                        user_features.append(prediction)
                        # write a row to the csv file
                        writer.writerow(user_features)

                        # close the file
                        bot_file.close()
                    except FileNotFoundError as e:
                        print("File not found: ",e)
                    if prediction==0:
                        print('Added')
                        collection.insert_one({'tweet':tweet['full_text'],'language':tweet['lang'],'created_at':str(datetime.strptime(tweet['created_at'],'%a %b %d %X %z %Y').replace(tzinfo=None).date()),'topic':q_obj['topic'],'query':q_obj['query']})
                    
                print('Number of tweets: '+str(count))
        except Exception as e:
            print('Failure occured \n Reason :',e)

    def load_bot_model(self,fname):
        model = XGBClassifier()
        try: 
            model.load_model(fname)
        except FileNotFoundError as e:
                print("File not found: ",e)
        return model
    
    def clean_data(self):
        collection = self.get_db_connection('tweets_data')
        tweets = list(collection.find())
        s = set()
        cleant_arr = []
        print(len(tweets))
        for tweet in tweets:
            if tweet['tweet'] not in s:
                s.add(tweet['tweet'])
                cleant_arr.append(tweet)
        try:
            file = open("file1.txt", "w+")
            
            # Saving the array in a text file
            content = str(cleant_arr)
            file.write(content)
            file.close()
        except FileNotFoundError as e:
            print("File not found: ",e)
        print(len(cleant_arr))
        collection.drop()
        count_of_tweets = 0
        for tweet in cleant_arr:
            count_of_tweets+=1
            collection.insert_one(tweet)
            print(count_of_tweets)
        
