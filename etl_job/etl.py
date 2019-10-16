from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pymongo import MongoClient
from sqlalchemy import create_engine
import time
# import random

# Wait 1 minute before starting this script so that there is input in MongoDB
time.sleep(120)

## Set up connection to postgres
engine = create_engine('postgresql://postgres:postgres@postgresdb:5432/twitterdb')
engine.execute("""CREATE TABLE IF NOT EXISTS tweets
                    (id SERIAL primary key,
                    text VARCHAR(500),
                    sentiment FLOAT(8));""")

## Set up connection to MongoDB
connection_string = 'mongodb'
conn = MongoClient(connection_string)

## Initialize the twitterdata database and the tweets collection
db = conn.twitterdata # Define database to switch to/create if not already available
collection = db.tweets # Define collection to switch to/create if not already available

## Instantiate the Sentiment analysis neural net model
s = SentimentIntensityAnalyzer()

def get_tweet():
    tweets = list(collection.find())
    tweet = tweets[1]
    return tweet["text"]

def vader(tweet):
    if tweet:
        score = s.polarity_scores(tweet)['compound']
        return score
    else:
        return 0

def write_to_postgres(tweet, sentiment):
    engine.execute(f"INSERT INTO tweets (text, sentiment) VALUES ('{tweet}', {sentiment});")

#engine.execute(f"INSERT INTO tweets (text, sentiment) VALUES ('test', 'test_score');")

for i in range(3):
   new_tweet = get_tweet()
   print('Tweet loaded from MongoDB')
   sentiment = vader(new_tweet)
   print('VaderSentiment ran successfully')
   write_to_postgres(new_tweet, sentiment)
   print('Output inserted into Postgres')
