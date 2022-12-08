# TweetMind

## Twitter Sentiment Analysis
Sentiment analysis is a Natural Language Processing (NLP) technique to determine the sentiment of a particular tweet is positive, negative or neutral. 

## Introduction
The main aim of this project is to identify specific topics in Twitter and to analyze whether the varying sentiments of the people with respect to that topic. Common issues that trend in Twitter are climate change, self-driving cars, election results, etc. and 

## Data Cleaning
Each tweet is cleaned and preprocessed to remove special characters, extra spaces, emojis, hashtags & mentions etc. Cleaning is important for text classification as it is easier for a model to extract information from cleaned tweets. If this step is skipped, then there is a high possibility of working with noisy or inconsistent data. 

## Approach
There are two files related to text classification. The trained_on_datasets.ipynb file is a step by step process of training BERT and RoBERTa models on the SemEval 2017 dataset. Although BERT and RoBERTa are pretrained datasets, they are used as a base model upon which additional layers are added to further fine-tune the model for better accuracy. The training set of SemEval 2014 Task 4 - Subtask A consists of 6000 samples, test set consists of 20632 samples and the validation set contains 2000 samples. The training set of 6000 samples has an uneven distribution of positive, negative and neutral sentiments which is why oversampling is done to ensure that there are equal samples of each sentiment. If oversampling is not done, then there is a high probability that the model will not recognize or classify the tweets which have the least number of sentiments. 

Naive Bayes Classifier is used as a baseline model and we get an accuracy of 50% on the test set. The BERT model reports an accuracy of 59%, therefore being better than the baseline model whereas RoBERTa reports an accuracy of 66% which outperforms all others. Since the RoBERTa model is pretrained on tweets and their sentiments, it makes sense that fine-tuning this model will give better results than others. 

The other file of pretrained_models.ipynb contains models of RoBERTa, XLM-R and Happy Transformer which are used to directly obtain the score of whether a tweet is positive, negative or neutral. It can be classified on live data. XLM-R is a model pre-trained on multilingual languages and canhence determine the sentiment in any of the 8 languages it has been trained on. Lastly, the Happy Transformer is a package built on top of the Hugging Face library which allows us to use any state-of-the-art NLP models. We have used the DistilBERT model to classify the text and determine the model. Each of these pre-trained models give good results in identifying the sentiment, but there are a few tweets that these models fail to predict accurately. 

Some of those tweets are:
1. @ChrisCuomo Thank you for handling these climate change deniers so beautifully. These people make me sick. Such sellouts. [Negative instead of Positive]
2. @turnflblue What we need is all powerful czar. One that can, in the name of climate change, dictate our lives for us. Sign me up! [Neutral instead of Negative]
3. Two places I'd invest all my money if I could: 3D printing and Self-driving cars!!! [Neutral instead of Positive]
4. #AAPL:The 10 best Steve Jobs emails ever...http://t.co/82G1kL94tx [Positive instead of neutral]

## Observations
Having tried other models such as SVM, VADER, CNN, we have observed that the pretrained models of RoBERTa, XLM-R outperforms most. Choosing the best model and classifying each live tweet will be done to perform analysis and visualization for understanding topics with their sentiment distribution.  