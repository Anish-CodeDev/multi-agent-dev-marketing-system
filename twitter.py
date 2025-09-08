import tweepy
import os
from dotenv import load_dotenv
from gemini import extract_topics_from_tweets
load_dotenv()
token = os.environ['BEARER_TOKEN']

client = tweepy.Client(bearer_token=token)

def retrieve_tweets_by_query(query):
    query =f"{query} lang:en -is:retweet"
    tweets = client.search_recent_tweets(query=query,max_results=10)
    data = []

    for tweet in tweets.data:
        data.append(tweet.text)
    return data
data = retrieve_tweets_by_query("AI")

print(extract_topics_from_tweets(data))