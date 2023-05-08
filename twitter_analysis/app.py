from flask import Flask, jsonify, render_template
import csv
import os 
app = Flask(__name__)
import warnings
warnings.filterwarnings("ignore")
from tweet_class import TweetCollection

# This is the main route of the application
# Using this, we land on the main UI
@app.route('/')
def index():
    return render_template('base.html')

# This is endpoint is used for the tweet fetching pipeline
@app.route('/getTweets')
def getTweets():
    twitobj = TweetCollection()
    twitobj.get_tweets()
    return 'Hi'

# This is used for deduplication of the data
@app.route('/cleanTweets')
def cleanTweets():
    twitobj = TweetCollection()
    twitobj.clean_data()
    return 'Cleaning Done'

@app.route('/getChartData')
def getChartData():
    twitobj = TweetCollection()
    graph_data = twitobj.get_topic_data()
    return jsonify(graph_data)


# This endpoint is used for converting data from MongoDB into csv files
@app.route('/convertData')
def convertData():
    twitobj = TweetCollection()
    try: 
        collection = twitobj.get_db_connection('tweets_data')
        topics = ['Academic Workers Strike','Climate Change','Russia Ukraine War','Layoffs','Gun Violence']
        for topic in topics:
            headers = ['Id','Tweet','Language','Created At','Topic','Query','Retweet Count','Tweet Id']
            tweets = collection.find({"retweet_count": { "$ne": None },"tweet_id": { "$ne": None },"topic":topic})
            try:
                topic_file = open(topic+'.csv', 'w+')
                writer = csv.writer(topic_file)
                # write a row to the csv file
                writer.writerow(headers)
                for tweet in tweets:
                    print("{}".format(tweet['tweet_id']))
                    writer.writerow([tweet['_id'],tweet['tweet'],tweet['language'],tweet['created_at'],tweet['topic'],tweet['query'],tweet['retweet_count'],"{}".format(tweet['tweet_id'])])
                topic_file.close()
            except FileNotFoundError as e:
                print("File not found: ",e)
                return
        return 'Converted'
    except Exception as e:
        return ("Exception occured: ",e)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run()