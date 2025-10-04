import tweepy
import os
from dotenv import load_dotenv
from gemini import extract_topics_from_tweets
load_dotenv()
token = os.environ['BEARER_TOKEN']
api_key = os.environ['API_KEY'] 
api_secret = os.environ['API_SECRET'] 
access_token = os.environ['ACCESS_TOKEN'] 
access_token_secret = os.environ['ACCESS_TOKEN_SECRET'] 
client = tweepy.Client(bearer_token=token)

def retrieve_tweets_by_query(query):
    query =f"{query} research, products lang:en -is:retweet"
    tweets = client.search_recent_tweets(query=query,max_results=10)
    data = []

    for tweet in tweets.data:
        data.append(tweet.text)
    return data

def post_tweets(text):
    client = tweepy.Client(consumer_key=api_key,
                            consumer_secret=api_secret,
                            access_token=access_token,
                            access_token_secret=access_token_secret)
    res = client.create_tweet(text=text)

#post_tweets("Posted using python")