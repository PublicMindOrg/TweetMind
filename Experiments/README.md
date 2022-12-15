# TweetMind

Sentiment analysis is a Natural Language Processing (NLP) technique to determine the sentiment of a particular tweet is positive, negative or neutral. 

## Introduction
The main aim of this project is to identify specific topics in Twitter and to analyze whether the varying sentiments of the people with respect to that topic. Common issues that trend in Twitter are climate change, self-driving cars, election results, etc. 

## Data Cleaning
Each tweet is cleaned and preprocessed to remove special characters, extra spaces, emojis, hashtags & mentions etc. Cleaning is important for text classification as it is easier for a model to extract information from cleaned tweets. If this step is skipped, then there is a high possibility of working with noisy or inconsistent data. 

## Approach
BERT and RoBERTa are trained and tested on the SemEval 2017 - Task 4 dataset to achieve an accuracy of 59% and 66% respectively. The SemEval 2017 is a benchmarked dataset containing about 6000 training samples, 20632 testing samples and 2000 validation samples. The training data is oversampled to achieve accurate results. Naive Bayes Classifier is used as a baseline model and we get an accuracy of 50% on the test set. Since the RoBERTa model is pretrained on tweets and their sentiments, it makes sense that fine-tuning this model will give better results than others. 

The other file of pretrained_models.ipynb contains models of RoBERTa, XLM-R and Happy Transformer which are used to directly obtain the score of whether a tweet is positive, negative or neutral. It can be classified on live data. XLM-R is a model pre-trained on multilingual languages and canhence determine the sentiment in any of the 8 languages it has been trained on. Lastly, the Happy Transformer is a package built on top of the Hugging Face library which allows us to use any state-of-the-art NLP models. We have used the DistilBERT model to classify the text and determine the model. Each of these pre-trained models give good results in identifying the sentiment, but there are a few tweets that these models fail to predict accurately. 

Some of those tweets are:
1. @ChrisCuomo Thank you for handling these climate change deniers so beautifully. These people make me sick. Such sellouts. [Negative instead of Positive]
2. @turnflblue What we need is all powerful czar. One that can, in the name of climate change, dictate our lives for us. Sign me up! [Neutral instead of Negative]
3. Two places I'd invest all my money if I could: 3D printing and Self-driving cars!!! [Neutral instead of Positive]
4. #AAPL:The 10 best Steve Jobs emails ever...http://t.co/82G1kL94tx [Positive instead of neutral]

## Stance Detection
The SemEval 2016 - Detecting Stance in Tweets dataset was used to train-test the BERT and RoBERTa models thereby achieving accuracies of 50% and 56% respectively. The pretrained PoliBERTweet stance transformer model by HuggingFace is trained only on specific political individuals such as Joe Biden and Donald Trump. Testing this model on the Stance dataset with only Trump and Hillary Clinton gave about a 43% accuracy in the results.

Tweets that didn't work:
1. @ABC Stupid is as stupid does! Showedhis true colors; seems that he ignores that US was invaded, & plundered,not discovered #SemST [NONE instead of AGAINST]
2. @RSherman_25 Join Twitter Trump brigade #onethousandtweets to support message #MakeAmericaGreatAgain @realDonaldTrump #SemST [NONE instead of FAVOR]
3. @realDonaldTrump we all want you as the next president !! You tell it has it is and not as a spineless politician! #SemST [AGAINST instead of FAVOR]

## Observations
The pretrained models are faster and easier to run as they just needed to be executed as an inference. Training models like BERT, RoBERTa etc. on the datasaets are time-consuming and computationally expensive. Stance detection will have to be used only for political tweets due to lack of stance related pretrained BERT models. 