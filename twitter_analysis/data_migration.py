import csv
from decouple import config
from pymongo import MongoClient
cluster = MongoClient(config('MONGO_URL'))
db = cluster['TweetMind']
collection = db['tweets_data']
topics = ['Academic Workers Strike','Climate Change','Russia Ukraine War']
for i in topics:
    headers = ['Id','Tweet','Language','Created At','Topic','Query']
    tweets = list(collection.find({'topic':i}))
    f = open(i+'.csv', 'a')
    writer = csv.writer(f)
    # write a row to the csv file
    writer.writerow(headers)
    for tweet in tweets:
        writer.writerow([tweet['_id'],tweet['tweet'],tweet['language'],tweet['created_at'],tweet['topic'],tweet['query']])

    # close the file
    f.close()
    