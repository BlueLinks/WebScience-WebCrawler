import pymongo
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import adjusted_rand_score
import re
from collections import Counter
import pandas as pd

client = pymongo.MongoClient('localhost', 27017)
db = client.TwitterStream
tweets = db.all_tweets

documents = []

username_data = []
hashtag_data = []


if __name__ == "__main__":
    print("=== Retrieving tweets from database ===")

    tweets = tweets.find().limit(50000)

    for tweet in tweets:
        try:
            documents.append(tweet['text'])
        except:
            pass


    print("=== Vectorising ===")
    vectorizer = TfidfVectorizer(analyzer='word', stop_words="english")
    X = vectorizer.fit_transform(documents)

    true_k = 6
    print("=== Preforming KMeans with %d clusters ===" % true_k)
    model = KMeans(n_clusters=true_k, init='random', max_iter=300, n_init=10)
    model.fit(X)

    print("Top terms per cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(true_k):
        print("=== Cluster %d, Size: %d ===" % (i,len(order_centroids[i])))
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind])