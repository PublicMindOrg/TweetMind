from decouple import config
from apscheduler.schedulers.background import BackgroundScheduler
from pymongo import MongoClient
import requests
from datetime import datetime
import pickle
import numpy as np
import pandas as pd
from collections import deque
sched = BackgroundScheduler(daemon=True)

def load_pkl(fname):
    with open(fname, 'rb') as f:
        obj = pickle.load(f)
    return obj

query_list = deque([{'topic': 'Climate Change', 'query': 'climate change'}, {'topic': 'Climate Change', 'query': 'climate crisis'}, {'topic': 'Climate Change', 'query': 'climate emergency'}, {'topic': 'Climate Change', 'query': 'climate action'}, {'topic': 'Climate Change', 'query': 'global warming'}, {'topic': 'Climate Change', 'query': 'anthropogenic warming'}, {'topic': 'Climate Change', 'query': 'fossil fuels'}, {'topic': 'Climate Change', 'query': 'carbon footprint'}, {'topic': 'Climate Change', 'query': 'carbon neutral'}, {'topic': 'Climate Change', 'query': 'carbon sink'}, {'topic': 'Climate Change', 'query': 'carbon release'}, {'topic': 'Climate Change', 'query': 'carbon capture'}, {'topic': 'Climate Change', 'query': 'carbon credit'}, {'topic': 'Climate Change', 'query': 'carbon climate'}, {'topic': 'Climate Change', 'query': 'carbon tax'}, {'topic': 'Climate Change', 'query': 'extreme weather'}, {'topic': 'Climate Change', 'query': 'methane'}, {'topic': 'Climate Change', 'query': 'green energy'}, {'topic': 'Climate Change', 'query': 'green growth'}, {'topic': 'Climate Change', 'query': 'green jobs'}, {'topic': 'Climate Change', 'query': 'greenhouse gas'}, {'topic': 'Climate Change', 'query': 'greenhouse gasses'}, {'topic': 'Climate Change', 'query': 'greenhouse effect'}, {'topic': 'Climate Change', 'query': 'degrowth,sustainable climate'}, {'topic': 'Climate Change', 'query': 'sustainability climate'}, {'topic': 'Climate Change', 'query': 'sea level rise'}, {'topic': 'Climate Change', 'query': 'net zero'}, {'topic': 'Climate Change', 'query': 'destination zero'}, {'topic': 'Climate Change', 'query': 'climate denial'}, {'topic': 'Climate Change', 'query': 'climate denialism'}, {'topic': 'Climate Change', 'query': 'climate change denial'}, {'topic': 'Climate Change', 'query': 'climate denier'}, {'topic': 'Climate Change', 'query': 'climate change denier'}, {'topic': 'Climate Change', 'query': 'climate skeptic'}, {'topic': 'Climate Change', 'query': 'climate change skeptic'}, {'topic': 'Climate Change', 'query': 'climate scam'}, {'topic': 'Climate Change', 'query': 'climate cult'}, {'topic': 'Climate Change', 'query': 'climate misinformation'}, {'topic': 'Climate Change', 'query': 'free market'}, {'topic': 'Climate Change', 'query': 'CO2 climate '}, {'topic': 'Climate Change', 'query': 'renewable energy'}, {'topic': 'Climate Change', 'query': 'renewables'}, {'topic': 'Russia Ukraine War', 'query': 'Russia Ukraine war'}, {'topic': 'Russia Ukraine War', 'query': 'Russo-Ukrainian war'}, {'topic': 'Russia Ukraine War', 'query': 'Russian Ukrainian war'}, {'topic': 'Russia Ukraine War', 'query': 'Ukraine war'}, {'topic': 'Russia Ukraine War', 'query': 'Ukrainian war'}, {'topic': 'Russia Ukraine War', 'query': 'Putin Ukraine'}, {'topic': 'Russia Ukraine War', 'query': 'Putin Ukrainian'}, {'topic': 'Russia Ukraine War', 'query': 'Zelensky Russia'}, {'topic': 'Russia Ukraine War', 'query': 'Zelenskiy Russia'}, {'topic': 'Russia Ukraine War', 'query': 'Zelensky war'}, {'topic': 'Russia Ukraine War', 'query': 'Zelenskiy war'}, {'topic': 'Academic Workers Strike', 'query': 'academic workers strike'}, {'topic': 'Academic Workers Strike', 'query': 'academic workers labor'}, {'topic': 'Academic Workers Strike', 'query': 'academic workers organize'}, {'topic': 'Academic Workers Strike', 'query': 'academic workers union'}, {'topic': 'Academic Workers Strike', 'query': 'university workers strike'}, {'topic': 'Academic Workers Strike', 'query': 'university workers labor'}, {'topic': 'Academic Workers Strike', 'query': 'university workers organize'}, {'topic': 'Academic Workers Strike', 'query': 'university workers union'}, {'topic': 'Academic Workers Strike', 'query': 'college workers strike'}, {'topic': 'Academic Workers Strike', 'query': 'college workers labor'}, {'topic': 'Academic Workers Strike', 'query': 'college workers organize'}, {'topic': 'Academic Workers Strike', 'query': 'college workers union'}, {'topic': 'Academic Workers Strike', 'query': 'higher education workers strike'}, {'topic': 'Academic Workers Strike', 'query': 'higher education workers labor'}, {'topic': 'Academic Workers Strike', 'query': 'higher education workers organize'}, {'topic': 'Academic Workers Strike', 'query': 'higher education workers union'}, {'topic': 'Academic Workers Strike', 'query': 'academic employees strike'}, {'topic': 'Academic Workers Strike', 'query': 'academic employees labor'}, {'topic': 'Academic Workers Strike', 'query': 'academic employees organize'}, {'topic': 'Academic Workers Strike', 'query': 'academic employees union'}, {'topic': 'Academic Workers Strike', 'query': 'university employees strike'}, {'topic': 'Academic Workers Strike', 'query': 'university employees labor'}, {'topic': 'Academic Workers Strike', 'query': 'university employees organize'}, {'topic': 'Academic Workers Strike', 'query': 'university employees union'}, {'topic': 'Academic Workers Strike', 'query': 'college employees strike'}, {'topic': 'Academic Workers Strike', 'query': 'college employees labor'}, {'topic': 'Academic Workers Strike', 'query': 'college employees organize'}, {'topic': 'Academic Workers Strike', 'query': 'college employees union'}, {'topic': 'Academic Workers Strike', 'query': 'higher education employees strike'}, {'topic': 'Academic Workers Strike', 'query': 'higher education employees labor'}, {'topic': 'Academic Workers Strike', 'query': 'higher education employees organize'}, {'topic': 'Academic Workers Strike', 'query': 'higher education employees union'}, {'topic': 'Academic Workers Strike', 'query': 'student workers strike'}, {'topic': 'Academic Workers Strike', 'query': 'student workers labor'}, {'topic': 'Academic Workers Strike', 'query': 'student workers organize'}, {'topic': 'Academic Workers Strike', 'query': 'student workers union'}, {'topic': 'Academic Workers Strike', 'query': 'student employees strike'}, {'topic': 'Academic Workers Strike', 'query': 'student employees labor'}, {'topic': 'Academic Workers Strike', 'query': 'student employees organize'}, {'topic': 'Academic Workers Strike', 'query': 'student employees union'}])

def get_tweets():
    sched.add_job(get_all_tweets,'interval',minutes=1,replace_existing=True)
    sched.start()
    return get_all_tweets()

def get_all_tweets():
    query_params = ''
    TWITTER_API_1 = config('TWITTER_API_1')
    q_obj = query_list.popleft()
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
    param = tweets['search_metadata']['next_results']
    q_obj['next_results'] = param +'&tweet_mode=extended'
    query_list.append(q_obj)
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
        average_tweets_per_day = np.round(statuses_count / account_age_days, 3)

        # manufactured features
        hour_created = int(datetime.strptime(user['created_at'],'%a %b %d %X %z %Y').replace(tzinfo=None).strftime('%H'))
        network = np.round(np.log(1 + friends_count)
                           * np.log(1 + followers_count), 3)
        tweet_to_followers = np.round(
            np.log(1 + statuses_count) * np.log(1 + followers_count), 3)
        follower_acq_rate = np.round(
            np.log(1 + (followers_count / account_age_days)), 3)
        friends_acq_rate = np.round(
            np.log(1 + (friends_count / account_age_days)), 3)

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
        # xgb_model = load_pkl('model.pickle')
        # print(xgb_model)
        # prediction = xgb_model.predict(user_df)[0]
        # print(prediction)
        collection.insert_one({'tweet':i['full_text'],'language':i['lang'],'created_at':i['created_at'],'topic':q_obj['topic'],'query':q_obj['query']})
    return 'Number of tweets: '+str(count)
    
        
    
    

if __name__ == '__main__':
    # port = int(os.environ.get('PORT', 5000))
    #app.run()
    get_all_tweets()
    