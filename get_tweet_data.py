import pymongo
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import datetime
import time
import sys

client = pymongo.MongoClient('localhost', 27017)
db = client.TwitterStream
db.tweets.create_index("id", unique=True, dropDups=True)
all_collection = db.all_tweets

# Add the keywords you want to track.
keywords = ['trump','biden','republican','democrat',"bernie",'bernie sanders','sanders','joe','donald','presidential election','@realDonaldTrump','#PresidentialRace2020','#PresidentialPrimary','@BernieSanders','Bill','@JoeBiden','@SenSanders','#2020election']

users = ['25073877','216776631', '939091']


with open('keys.txt', 'r') as f:
    lines = f.readlines()
    consumer_key = lines[0].rstrip()
    consumer_secret = lines[1].rstrip()
    access_token = lines[2].rstrip()
    access_token_secret = lines[3].rstrip()


# Tweet Listener
class StdOutListener(StreamListener):

    def __init__(self, time_limit = 60):
        # time_limit is time in minutes
        self.duplicates = 0
        self.limit = (time_limit * 60)
        self.start_time = time.time()

    def on_data(self, data):
        if (time.time() - self.start_time) < self.limit:
            # Load the Tweet into the variable "tweet"
            tweet = json.loads(data)
            try:
                all_collection.insert_one(tweet)
                return True
            except:
                # This is a duplicate
                self.duplicates += 1
                print("Duplicates so far: %d" % self.duplicates)
        else:
            # Times Up
            return False

    # Prints the reason for an error to your console
    def on_error(self, status):
        print(status)


# Some Tweepy code that can be left alone. It pulls from variables at the top of the script
if __name__ == '__main__':
    listener = StdOutListener()
    try:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        print("AUTH SUCCESS")
    except:
        print("AUTH FAILED")
        sys.exit()

    stream = Stream(auth, listener)
    print("Starting Streaming for %s seconds" % listener.limit)
    stream.filter(follow=users, track=keywords, languages=["en"],is_async=True)
    print(listener.duplicates)
