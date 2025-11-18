import tweepy
import os
from dotenv import load_dotenv
from gemini import extract_topics_from_tweets
from pytrends.request import TrendReq   
load_dotenv()
token = os.environ['BEARER_TOKEN']

client = tweepy.Client(bearer_token=token)

def retrieve_tweets_by_query(query):
    '''query =f"{query} research, products lang:en -is:retweet"
    tweets = client.search_recent_tweets(query=query,max_results=10)
    data = []

    for tweet in tweets.data:
        data.append(tweet.text)'''
    pytrends = TrendReq()
    pytrends.build_payload(kw_list=[query],cat=5,timeframe='now 7-d')
    data = pytrends.related_queries()
    df = data[query]['top']
    data = list(df['query'])
    return data


def post_tweets(text):
    api_key = os.environ['API_KEY'] 
    api_secret = os.environ['API_SECRET'] 
    access_token = os.environ['ACCESS_TOKEN'] 
    access_token_secret = os.environ['ACCESS_TOKEN_SECRET'] 
    client = tweepy.Client(consumer_key=api_key,
                            consumer_secret=api_secret,
                            access_token=access_token,
                            access_token_secret=access_token_secret)
    print(len(text))
    res = client.create_tweet(text=text)
    return "Done"

#post_tweets("Posted using python")
if __name__ == "__main__":

    print(post_tweets("Agentic AI"))