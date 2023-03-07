from flask import Flask, render_template
import csv
import os 
app = Flask(__name__)
import warnings
warnings.filterwarnings("ignore")
from tweet_class import TweetCollection


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
    twitobj = TweetCollection()
    try: 
        collection = twitobj.get_db_connection()
        topics = ['Academic Workers Strike','Climate Change','Russia Ukraine War','Layoffs','Gun Violence']
        for topic in topics:
            headers = ['Id','Tweet','Language','Created At','Topic','Query']
            tweets = list(collection.find({'topic':topic}))
            try:
                topic_file = open('./folder_1/'+topic+'.csv', 'w+')
                writer = csv.writer(topic_file)
                # write a row to the csv file
                writer.writerow(headers)
                for tweet in tweets:
                    writer.writerow([tweet['_id'],tweet['tweet'],tweet['language'],tweet['created_at'],tweet['topic'],tweet['query']])
                topic_file.close()
            except FileNotFoundError as e:
                print("File not found: ",e)
                return
        return 'Converted'
    except Exception as e:
        print("Exception occured: ",e)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run()