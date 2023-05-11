import platform; print(platform.platform())
import sys; print("Python", sys.version)
import scipy; print("SciPy", scipy.__version__)
import os
import pandas as pd
import re, string
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
from flask import Flask
import torch
from pymongo import MongoClient
import pandas as pd 
import sys

app = Flask(__name__)

def data_cleaning(line):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            "]+", flags = re.UNICODE)
    clean_text = regrex_pattern.sub(r'', line)
    clean_text = clean_text.replace('\r', '').replace('\n', ' ').replace('\n', ' ').lower() #remove \n and \r and lowercase
    clean_text = re.sub(r"(?:\@|https?\://)\S+", "", clean_text) #remove links and mentions
    clean_text = re.sub(r'[^\x00-\x7f]',r'', clean_text) #remove non utf8/ascii characters such as '\x9a\x91\x97\x9a\x97'
    banned_list= string.punctuation + 'Ã'+'±'+'ã'+'¼'+'â'+'»'+'§'
    table = str.maketrans('', '', banned_list)
    clean_text = clean_text.translate(table)
    new_tweet = " ".join(word.strip() for word in re.split('#(?!(?:hashtag)\b)[\w-]+(?=(?:\s+#[\w-]+)*\s*$)', clean_text)) #remove last hashtags
    new_tweet2 = " ".join(word.strip() for word in re.split('#|_', new_tweet)) #remove hashtags symbol from words in the middle of the sentence
    new_tweet2 = re.sub("\s\s+" , " ", new_tweet2)
    clean_text = new_tweet2.replace('$', '')
    clean_text = clean_text.replace('#', '')
    return clean_text

def label_tweet(enc_tweet):
  enc = enc_tweet
  output = model(**enc)
  scores = output[0][0].cpu().detach().numpy()
  scores = softmax(scores)
  map_idx = scores.argmax(axis=0)
  lbl = labels[map_idx]
  return lbl

def insertToMongo(reader):
    cluster = MongoClient('mongodb+srv://publicmind3:publicmind2@cluster0.dr4qqbc.mongodb.net/?retryWrites=true&w=majority')
    db = cluster['TweetMind']
    collection = db['results_new']
    mongo_docs = []

    for tweet in reader:
        mongo_docs.append(tweet)
    collection.insert_many(mongo_docs)

@app.route("/")
def inference():
    global labels, model

    with open('./data/Climate Change.csv') as f:

        fpath = './data/'
        output_path = os.path.join(fpath, 'output.csv')
        print(output_path, "\n")

        data_test = pd.read_csv(f, encoding='latin-1')
        print(data_test.head())


        data_test.drop_duplicates(subset=['Tweet'], inplace=True)
        data_test.reset_index(drop=True, inplace=True)
        # print("dropped duplicates")

        data_test['clean_text'] = data_test['Tweet'].apply(lambda func: data_cleaning(func))
        # print("data cleaning done\n")

        model = AutoModelForSequenceClassification.from_pretrained('./roberta-model/')
        tokenizer = AutoTokenizer.from_pretrained('./roberta-tokenizer/')
        labels = [-1, 0, 1]

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model.to(device)

        data_test['encoded_tweet'] = data_test['clean_text'].apply(lambda func: tokenizer(func, return_tensors='pt'))
        # print("data encoding done\n")

        for k,v in data_test['encoded_tweet'].items():
            data_test['encoded_tweet'][k] = v.to(device)
        # print("encoding to gpu done")

        data_test['predicted'] = ''

        data_test['predicted'] = data_test['encoded_tweet'].apply(lambda func: label_tweet(func))
        # print("data labelling done\n")

        # print("\n", output_path, "\n")
        df = data_test[['Tweet', 'Created At', 'Topic', 'Retweet Count', 'Tweet Id', 'predicted']]

        insertToMongo(df)

    return 'Done'

if __name__ == '__main__':
    app.run(host='0.0.0.0')