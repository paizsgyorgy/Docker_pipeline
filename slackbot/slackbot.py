import slack
from slacktoken import token_1, token_2
from sqlalchemy import create_engine
import time

time.sleep(120)

## Set up connection to postgres: Select 1) or 2) according to need
# 1) Connect to local postgres (ONLY FOR TESTING)
#engine = create_engine('postgresql://localhost:5432/twitter')

# 2) Connect to DB running in a docker container (FOR PRODUCTION)
engine = create_engine('postgresql://postgres:postgres@postgresdb:5432/twitterdb')

# Twitter connection
client = slack.WebClient(token=token_2)

# Load one tweet from postgresdb
def load_tweet():
    result = engine.execute("""SELECT text FROM tweetdata LIMIT 1;""")
    for tweet in result:
        return tweet

# Generate message
def generate_slackmessage(tweet_text):
    TEXT = f"""Hello from Docker! This is the latest Twitter message that contains the word Python: {tweet_text}"""
    return TEXT

# Define sleeptime for slackbot to wait between consequent messages
sleeptime = 60

# Run a while loop until the Docker container is shut down
while True:
    time.sleep(sleeptime)
    tweet = load_tweet()
    message = f"""Hello from Docker! This is the latest Twitter message that contains the word Python: {tweet}"""
    response = client.chat_postMessage(channel='#slack_bot', text=message)
