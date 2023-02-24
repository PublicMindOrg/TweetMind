# TweetMind
TweetMind is a project that analyzes public issues and gives a biased public overview on daily global crisis. We have started with 5 topics, Academic Workers Strike,Climate Change,Russia Ukraine War,Layoffs and Gun Violence. We have a dashboard where a user can see the analysis and certain endpoints for collecting tweets, storing them in the database, converting database-fetched tweeets to a dataframe, deduplication of tweets

## How to run the application?

  1. Build docker image by running the following command within the docker file directory. docker build --tag python-docker .
  2. Run this command to run the docker image: docker run -p 5000:5000 -t -i -v "$(pwd)/folder_1:/app/folder_1" python-docker:latest
  3. Open the browser http://127.0.0.1:5000 to get the Main UI page

## End Points
1. / (root): This is the landing page where the main UI code of the application runs. We have a single html file where a user selects a topic from the dropdown and we display the anaysis in the form of charts. The event handling is all done using jQuery. Charts are displayed using chart.js library. We fetch the results from the Machine Learning models and plot them based on the data and the particular topic

2. /getTweets: This endpoint is used to fetch tweets per topic and store them in the MongoDB database. We have all the seed terms stored in the topics.json file. We store them in a deque and continuously fetch new tweets from twitter. All the tweets are passed to a bot detector for filtering the real users and bots. We store all the results into a csv file called bot_data.csv, so that we can further use the data for analysis. The credentials and URL's are all stored in the .env file.

3. /cleanTweets: Sometimes, there are duplicate tweets being fetched multiple times. In order to remove them, we have added the deduplication code in cleanTweets endpoint. We just save the first instance of the tweets and eliminate the duplicate one's. Later, we delete the entire Database collection and adding the filtered tweets to the database again.

4. /convertData: This endpoint gets the topic-wise tweets from the MongoDB collections and stores them in topicwise CSV file to use them in the Machine Learning models. 