import tweepy
from decouple import config
from apscheduler.schedulers.background import BackgroundScheduler
from pymongo import MongoClient
from flask import Flask
import requests
import csv
app = Flask(__name__)
app.config['TESTING'] = True
app.config['FLASK_ENV'] = 'development'
app.config['DEBUG'] = True 
sched = BackgroundScheduler(daemon=True)

@app.route('/get_tweets/<string:query>')
def get_tweets(query):
    sched.add_job(get_all_tweets,'interval',args=[query],minutes=5,replace_existing=True)
    sched.start()
    # db = client.flask_db
    # print(db)
    return get_all_tweets(query)

def get_all_tweets(query):
    next_results = ''
    TWITTER_API_1 = config('TWITTER_API_1')
    query_params = "?q="+query+"&country_code=US&result_type=recent&count=100&language=en"
    headers = {'Authorization': config('API_TOKEN')}
    cluster = MongoClient('mongodb+srv://mehtaadi-1:Aditya3003@cluster0.ajx7zka.mongodb.net/?retryWrites=true&w=majority')
    db = cluster['TweetMind']
    collection = db['tweets_data']
    with open('./folder_1/tweet_data.csv', 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        count=0
        for j in range(100):
            api_url = TWITTER_API_1 + query_params
            if next_results!='':
                api_url = TWITTER_API_1 + next_results +'&language=en'
            tweets = requests.get(api_url,headers=headers).json()
            next_results = tweets['search_metadata']['next_results']
            for i in tweets['statuses']:
                count+=1
                collection.insert_one({'tweet':i['text'],'language':i['lang'],'created_at':i['created_at']})
                data = [i['text'],i['created_at'],i['lang']]
                writer.writerow(data)
    print(count)
    return 'Number of tweets: '+str(count)
            
    
        
    # client1 = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAGT8bgEAAAAAJZslobYs39BqCSVn%2BipiFNxH1ao%3D5osYxvUKqEteDrWV2eOFIQvABR1QCTy2RhHS450UwS6yTQuVlb')
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
    app.run()
    