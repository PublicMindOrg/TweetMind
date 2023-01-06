# TweetMind
This project is used for grabbing tweets pertaining to various topics and performs querying to extract the tweet information and stores them in MongoDB.

## How to run the application?

  1. Build docker image by running the following command within the docker file directory. docker build --tag tweet-app .
  2. Run this command to run the docker image docker run -it -v "$(pwd)/folder_1:/app/folder_1" tweet-app
  3. Open the docker application
  4. Check the current app running
  5. Open the CLI and run curl http://127.0.0.1:5000/get_tweets/{topic}
You can see the tweets updated in the Excel every 5 minutes

## Tweet Seed File

In this file, we have topics and each topic have multiple queries. Now, for each query we directly call the search API for the first time and store the next-results object of the response which will help us in obtaining the subsequent API results. This helps us in obtaining non-overlapping tweets. We have scheduler written in the code which runs the get_all_tweets function every 5 minutes and stores the result in MongoDB database cluster.

## MongoDB 

Once we login to the MongoDB account, we can go to our cluster and select the collection that we are using. Within the collection, we can look at tweets and filter them by any field.

This is the workflow of the application 
<img width="1323" alt="Screenshot 2022-12-20 at 3 42 39 PM" src="https://user-images.githubusercontent.com/32195607/211015002-8a36e31f-e0f5-41d5-b192-73feca3271d8.png">
