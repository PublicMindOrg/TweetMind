from decouple import config
from pymongo import MongoClient
import requests
import csv

def get_all_tweets(query):
    TWITTER_API_1 = config('TWITTER_API_1')
    query_params = "?q="+query+"&-filter:retweets&country_code=US&result_type=recent&count=100&lang=en"
    headers = {'Authorization': config('API_TOKEN')}
    cluster = MongoClient(config('MONGO_URL'))
    db = cluster['TweetMind']
    collection = db['tweets_data']
    
    count=0
    api_url = TWITTER_API_1 + query_params
    print(api_url)
    tweets = requests.get(api_url,headers=headers).json()
    for i in tweets['statuses']:
        count+=1
        collection.insert_one({'tweet':i['text'],'language':i['lang'],'created_at':i['created_at']})
    return 'Number of tweets: '+str(count)
            
    #TWEEPY 
        
    # client1 = tweepy.Client(bearer_token='')
    # header = ['Tweet', 'Date', 'Language']
    # filename = query+'.csv'
    # with open(filename, 'a', encoding='UTF8') as f:
    #     writer = csv.writer(f)
    #     count=0
    #     for tweet in tweepy.Paginator(client1.search_recent_tweets,query = query,
    #             tweet_fields= 'id,text,lang',
    #                                  max_results=100).flatten(limit=1000):
    #         # write the data
    #         print(tweet)
    #         count+=1
    #         print("Tweet added: ",count)
    #         data = [tweet.text,tweet.created_at,tweet.lang]
    #         writer.writerow(data)
    # return "Total tweets added:"+str(count)
    

if __name__ == '__main__':
    # port = int(os.environ.get('PORT', 5000))
    query = input('Enter your query term ')
    print(get_all_tweets(query))

    