import csv
from decouple import config
from pymongo import MongoClient
cluster = MongoClient(config('MONGO_URL'))
db = cluster['TweetMind']
collection = db['tweets_data']
tweets = list(collection.find({}))
with open('mongo_tweets.csv', 'a', encoding='UTF8') as f:
    writer = csv.writer(f)
    count=0
    for i in tweets:
        count+=1
        data = [i['tweet'],i['created_at'],i['language']]
        writer.writerow(data)
print(count)