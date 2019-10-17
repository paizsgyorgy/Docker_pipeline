from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pymongo import MongoClient
from sqlalchemy import create_engine
import time
import pandas as pd
# import random

# Wait 1 minute before starting this script so that there is input in MongoDB
time.sleep(60)

## Set up connection to postgres: Select 1) or 2) according to need
# 1) Connection to local postgres (ONLY FOR TESTING)
#engine = create_engine('postgresql://localhost:5432/twitter')

# 2) Connection to postgres running in docker container (FOR PRODUCTION)
engine = create_engine('postgresql://postgres:postgres@postgresdb:5432/twitterdb')

# Create table in database if it doesn't exist already


## Set up connection to MongoDB
# 1) Local mongodb connection (ONLY FOR TESTING)
#connection_string = 'mongodb://localhost:27017/'

# 2) Mongodb running in docker container
connection_string = 'mongodb'

conn = MongoClient(connection_string)

## Initialize the twitterdata database and the tweets collection
db = conn.twitterdata # Define database to switch to/create if not already available
collection = db.tweets # Define collection to switch to/create if not already available

## Instantiate the Sentiment analysis model
s = SentimentIntensityAnalyzer()

def get_tweets(n=1):
    """This function extracts last n number of tweets from mongodb"""
    tweets = list(collection.find())[-n:]
    return tweets

def vader(tweet, score):
    """This function runs vadersentiment on a tweet and returns a score"""
    if tweet:
        scores = s.polarity_scores(tweet)
        return scores[score]
    else:
        return 0


# def save_sentiment(tweet, sentiment):
#     """"This writes data into the postgres database"""
#     engine.execute(f"INSERT INTO tweets (text, sentiment) VALUES ('{tweet}', {sentiment});")

############################################################################

# Arrange last n tweets into dataframe
# tweets = get_tweets(n=1)
# cols = ['created_at', 'id', 'text', 'username', 'followers', 'user_favorites_count',
#         'retweets', 'favorites', 'hashtags', 'media_url', 'media_type', 'interesting']
# df = pd.DataFrame(tweets, columns=cols)
# df['sentiment_scores'] = df['text'].apply(vader)
# df.to_sql('tweetdata', con=engine, if_exists='append')

############################################################################

# Run in a loop until shut down
# Grabs last tweet in mongodb, applies vadersentiment and appends to sql database

while True:
    time.sleep(60)
    tweets = get_tweets(n=1)
    cols = ['created_at', 'id', 'text', 'username', 'followers', 'user_favorites_count',
            'retweets', 'favorites', 'hashtags', 'media_url', 'media_type', 'interesting']
    df = pd.DataFrame(tweets, columns=cols)
    df['sentiment_neg'] = df['text'].apply(vader, args=('neg',))
    df['sentiment_neu'] = df['text'].apply(vader, args=('neu',))
    df['sentiment_pos'] = df['text'].apply(vader, args=('pos',))
    df['sentiment_comp'] = df['text'].apply(vader, args=('compound',))
    df.to_sql('tweetdata', con=engine, if_exists='append')


############################################################################
#
# new_tweet = get_tweet()[-1]["text"]
# print('Tweet loaded from MongoDB')
# sentiment = vader(new_tweet)
# print('VaderSentiment ran successfully')
# write_to_postgres(new_tweet, sentiment)
# print('Output inserted into Postgres')
