from google import genai
from dotenv import load_dotenv
import base64
from github import Readme
load_dotenv()

client  = genai.Client()

def extract_topics_from_tweets(tweets):
    res = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[
            f"""
            You are given with a long list  of tweets, your job is to extract the key points from the tweets and respond with a list
            Tweets: {tweets}

            The response must be in the form a python list with several elements with no triple backticks
             """
        ]
    )
    print(res.text)
    return res.text

def extract_from_prompt(message):
    res = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[
            f"""
            From the user's prompt: {message}, extract the topic and respond only with that
            """
        ]
    )
    print(res.text)
    return res.text
def create_content_for_readme(old_content,topics):
    res = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[
            f"""
            You are given with the content of a README file of a particular repo. You are also given with a list of trending topics.
            Your job is to modify the contents of the readme file so that it suits the topics provided.

            content: {old_content}

            topics:{topics}
            """
        ]
    )
    return res.text

def decide_with_stars_are_less(stars):
    res = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[
            f"""
            You are given with a number of stars given for a repo, your job is to decide whether the number of stars are more or less
            Stars: {stars}
            If the stars are less respond with less otherwise responding with good
            """
        ]
    )
    return res.text
def generate_post(repo,platform):
    readme = Readme(repo)
    readme_content = readme.load_readme()
    res = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[
            f"""
            You are given with the contents of a readme file enclosed within triple backticks, your job is to generate content for a {platform} post.
            ```{readme_content}```
            Your job is to return a final post which can be directly posted on the platform: {platform}, don't include any additional text.
            
            The link to the repo will be https://github.com/{repo}

            Don't include multiple links to the repo.
            """
        ]
    )
    return res.text

#print(generate_post('Desktop_AI_Agent','dev.to'))