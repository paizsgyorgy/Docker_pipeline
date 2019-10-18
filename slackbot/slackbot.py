import slack
from slacktoken import token_1, token_2
from sqlalchemy import create_engine
import time

time.sleep(180)

## Set up connection to postgres: Select 1) or 2) according to need
# 1) Connect to local postgres (ONLY FOR TESTING)
#engine = create_engine('postgresql://localhost:5432/twitter')

# 2) Connect to DB running in a docker container (FOR PRODUCTION)
engine = create_engine('postgresql://postgres:postgres@postgresdb:5432/twitterdb')

# Twitter connection
client = slack.WebClient(token=token_2)

# Load tweets from postgresdb
def load_tweet(sql_statement):
    result = engine.execute(sql_statement)
    for tweet in result:
        return tweet

# Define statement to return last available tweet from the postgres database
statement = """ SELECT created_at, text, sentiment_comp
                FROM tweetdata
                ORDER BY created_at
                DESC LIMIT 1;"""

# Define sleeptime for slackbot to wait between consequent messages
sleeptime = 60

# Run a while loop until the Docker container is shut down
while True:
    tweet = load_tweet(statement)
    message = f"""Hello from Docker! This is the latest Twitter message that contains the word "Python": {tweet[1]}. The compound sentiment score of the tweet is: {tweet[2]}"""
    response = client.chat_postMessage(channel='#slack_bot', text=message)
    time.sleep(sleeptime)
