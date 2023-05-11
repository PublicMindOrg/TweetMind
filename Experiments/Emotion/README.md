# TweetMind

Emotion detection is an NLP technique to classify tweets as happy, sad, angry, fear, etc. 

### Introduction
In this project, we have tried Sentiment Analysis and Stance Detection. We will now be looking into Emotion Detection and the analysis of results of determing the tweets as one of the four emotions mentioned above. 

### Algorithms
The most commonly used algorithm was Long Short-Term Memory networks (LSTM). Some of the papers used LSTM with the dair-ai tweet dataset which gave great accuracy for tweets that were similar to the dataset. The tweets in the dataset were very straightforward and easy to understand. But when tested on our live data of Gun Violence, Climate Change etc. the algorithm was not giving good results due to the drastic change in language used. 

The dair-ai dataset had tweets like: 
- i feel strong and good overall
- i am feeling grouchy
- i didnt feel humiliated

Whereas the live data we were pulling from Twitter had tweet language like:
- "As gun violence continues to traumatize an entire generation of children, we must keep addressing the trauma kids are facing on a regular basis. Today I sat down with @SecBecerra @rep_jackson to discuss how we can help children cope with these experiences so they can thrive. https://t.co/JxiTHQ4B6s"

- "@1BethDutton @WASenDemocrats Washington state just relaxed gang and gang gun violence in school zones and other sensitive areas. Washington state doesn't care about actual gun crimes @GovInslee @WASenDemocrats https://t.co/vC8wQigbUR"

The difference in language made it difficult for the algorithm to classify the tweets correctly even though it was giving an 88% accuracy with the dair-ai dataset. Another paper showed that LSTM + GloVE was giving a 92.5% accuracy on 5 emotions, but at a deeper glance we noticed that the dataset was the same dair-ai one used. Concluding that the dataset is the reason we were not getting good enough results for the kind of data we were pulling, we researched through multiple dataset papers and found two whose language was most similar to our tweets. 

### Data Merging and Splitting
The two datasets found were to be merged and split in training and testing sets for the model. The following steps were followed to ensure that the data was handled accurately:
- Renamed columns for an easy merge
- Mapped emotion labels: happiness -> happy, sadness -> sad, hate -> angry and worry -> fear
- Selected similar number of emotions to have a balanced dataset
- Concatenated both datasets individually
- Split data 80:20 for each dataset and merged them to get an equal number of data from both

This merged data was used to train on an LSTM model which was further fine tuned by adding Dropout layers and the results were better than all other algorithms that were researched and tested. 

Some sample results are:
- @muskoka_mike2 @jack1492 @Charles02339637 Funny everything in the Democrats world is about race until we come to gun violence? We're not supposed to point that outÃ¢Â€Â¦. Why? Because it doesn't fit into their narrative/agenda! <b>[ANGRY]</b>

- @Jim_Jordan Remember the time a good guy with a gun stopped that one mass shooting? Yeah. I don't either. <b>[SAD]</b>

- "@ChrisMurphyCT @Morning_Joe ""How does a 17-year-old have 4 adult convictions (plus...) and still end up on felony probation, free to walk the streets? And what gun control law would stop him from illegally gaining possession of a firearm and using it in...a violent crime?""Criminalize criminals, not guns!!" <b>[FEAR]</b>

- "#Biden traveled to LA (a gun-free zone) to announce his gun control executive order. "[California has] got a higher-than-average mass public shooting per capita and they've got some of the strictest gun laws,"" Massie said. ""In fact, he (Biden) went to Los Angeles County. https://t.co/sxI1oQwqPe" <b>[HAPPY]</b>



 


