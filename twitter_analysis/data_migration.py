import csv
from pymongo import MongoClient
cluster = MongoClient('mongodb+srv://mehtaadi-1:Aditya3003@cluster0.ajx7zka.mongodb.net/?retryWrites=true&w=majority')
db = cluster['TweetMind']
collection = db['tweets_data']
tweets = list(collection.find({}))
with open('./folder_1/mongo_tweets.csv', 'a', encoding='UTF8') as f:
    writer = csv.writer(f)
    count=0
    for i in tweets:
        count+=1
        data = [i['tweet'],i['created_at'],i['language']]
        writer.writerow(data)
print(count)