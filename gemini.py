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

            Don't include multiple github links to the repo.
            """
        ]
    )
    return res.text


def decide_intermediate_step_using_msg(message,out_from_agent):
    res = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[
            f"""
            Given the user's request and previously completed action, suggest the next action from the below actions

            Please note that if {out_from_agent} indicated a negative feedback from the user  your action is 5, don't return anything else. 
            0 → Insight Agent - finds trending dev topics, keywords, opportunities.
            1 → Content Agent - Drafts changes for the readme files.
            2 → Design Helper Agent - creates diagrams, visuals, infographics.
            3 → Distribution Agent - posts/schedules across GitHub, LinkedIn, Twitter.
            4 → Feedback Agent - analyzes engagement (stars, likes, comments).
            5-> None of the above actions are suitable
            User's goal: {message}
            Output from agent: {out_from_agent}
            The regular flow is: generate insights->select repos which have less stars->modify the readme files->post on various platforms like twitter.
            Just return the index of the selected action without including any triple backticks
            """
        ]
    )
    return res.text
#print(generate_post('Desktop_AI_Agent','dev.to'))
print(decide_intermediate_step_using_msg("I want you to increase the popularity of all my repos","The user did'nt like any of the readme modifications"))