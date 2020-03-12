Web Science Twitter Crawler
================

 This is for the source code for my solution the Web Sciences (H) COMPSCI4077 coursework Network based Social Media Analytics
 
get_tweet_data.py
================

This script uses lists 'keywords' and 'users' to filter a stream of twitter data and insert the raw tweet json into a mongoDB collection TwitterStream.all_tweets

cluster_text.py
================

Simple script to find all tweets in TwitterStream.all_tweets and cluster all the text in the 'text' field into k categories and print the top 10 words used 

cluster.py
================

Similar to the 'cluster_text.py' script but instead of just the text this script extracts sernames and hashtags. To build this and the cluster_text.py scripts I used this stack overflow question as a reference https://stackoverflow.com/questions/27889873/clustering-text-documents-using-scikit-learn-kmeans-in-python

user_interactions.py
================
This is the most complex of the three and uses the networkx and matplot libraries to draw the user interaction graphs. Lines '63', '65', '67', and '69' can be commented in and out to control which interactions are graphed.

get_hashtags.py
================
This script is used to get the hashtag information from the 'TwitterStream.all_tweets' collection in format that is readable by https://www.cortext.net to produce graphs for the hashtag data.