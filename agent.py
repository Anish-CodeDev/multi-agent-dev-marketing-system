from typing import TypedDict,Sequence,Annotated
from dotenv import load_dotenv
from langgraph.graph import StateGraph,START,END
from langchain_core.messages import BaseMessage,SystemMessage,HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio
from google import genai
from gemini import extract_topics_from_tweets,extract_from_prompt,create_content_for_readme,decide_with_stars_are_less,generate_post
from twitter import retrieve_tweets_by_query,post_tweets
from github import Readme,list_repos,get_stars
from gemini import decide_intermediate_step_using_msg
load_dotenv()

client = genai.Client()

class AgentState(TypedDict):
    messages:Annotated[Sequence[BaseMessage],add_messages]

tools = []

graph = StateGraph(AgentState)
llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash')
def agent(state:AgentState):
    instruction = SystemMessage(content="""
        Consider the user's task and based on that:
        0 → Insight Agent - finds trending dev topics, keywords, opportunities.
        1 → Content Agent - Drafts changes for the readme files.
        2 → Design Helper Agent - creates diagrams, visuals, infographics.
        3 → Distribution Agent - posts/schedules across GitHub, LinkedIn, Twitter.
        4 → Feedback Agent - analyzes engagement (stars, likes, comments).
                                                                      
        Return with the index of the agent selected
            """)
    response = llm.invoke([instruction] + state['messages'])
    with open("data/user_ques.txt",'w') as f:
        f.write(state['messages'][-1].content)
    return {"messages":response}
def decide(state:AgentState):
    if state["messages"][-1].content == '0':

        return "insights"
    elif state["messages"][-1].content == '1':
        return "gen-content"
    elif state["messages"][-1].content == '2':
        return "design"
    elif state["messages"][-1].content == '3':
        return "posts"
    elif state["messages"][-1].content == '4':
        return "feedback"
    else:
        return "END"
graph.add_node("agent",agent)
def gen_content(state:AgentState):
    with open("data/insights.txt") as f:
        topics = f.read()
    
    #topics = eval(topics)
    # We're testing now
    #topics = ["Agentic AI","Usage of LLM's","LangGraph","Autonomous systems"]
    # Create a function in gemini two extract the repo link.
    repos = list_repos('Anish-CodeDev')
    for repo in repos:

        readme  = Readme(repo)
        content = readme.load_readme()
        new_content = create_content_for_readme(content,topics)
        print("I am suggesting an improvement, press Y if you like it and N if you don't like it")
        print(new_content)
        inp = input("Your choice: ")
        if inp == "Y":

        
            res = readme.update_readme(new_content)

        elif inp == "N":
            res = 'The user did\'nt like it'
            print(res)
    
    if res != 'The user did\'nt like it':
        return {"messages":"The user did'nt like it"}
    return {"messages":"The content of the README of the repo has been updated"}
def gen_insights(state:AgentState):
    topic = extract_from_prompt(state['messages'])
    tweets = retrieve_tweets_by_query(topic)
    topics = extract_topics_from_tweets(tweets)
    topics = eval(topics)
    with open("data/insights.txt",'a+') as f:
        for topic in topics:

            f.write(topics + '\n')

    return {"messages":"The insights have been generated."}
def gen_design(state:AgentState):
    return {"messages":"design"}
def posts(state:AgentState):
    with open("data/repos_to_publicise.txt",'r') as f:
        repos_list = f.read()
    
    repos_list = repos_list.split('\n')
    repos_list.remove('')
    for repo in repos_list:
        content = generate_post(repo,"X")
        print(content)
        decision = input("Press Y if you want me to publish the post and press N if you did'nt like the post")
        if decision == "Y":
            res = post_tweets(content)
    return {"messages":"The draft was shown to you and decision was taken based on their will"}
def manage_feedback(state:AgentState):
    starred = get_stars('Anish-CodeDev')
    with open('data/repos_to_publicise.txt','r+') as f:
        f.truncate(0)
    for repo in starred:
        decision = decide_with_stars_are_less(starred[repo])
        if decision == "less":
            with open('data/repos_to_publicise.txt','a') as f:
                f.write(repo + '\n')
        else:
            print('It was good')
    return {"messages":"The repos with less numbers of stars have been noted"}
graph.add_node("gen_insights",gen_insights)
graph.add_node("content",gen_content)
graph.add_node("design",gen_design)
graph.add_node("posts",posts)
graph.add_node("feedback",manage_feedback)
graph.add_edge(START,"agent")
# Later add a return value for communication between agents
graph.add_conditional_edges(
    "agent",
    decide,
    {
        "gen-content":"content",
        "insights":"gen_insights",
        "design":"design",
        "posts":"posts",
        "feedback":"feedback",
        "END":END
    }
)
# When things start working also trying to loop the agent communication
graph.add_edge("content","intermediate")
graph.add_edge("gen_insights","intermediate")
graph.add_edge("design","intermediate")
graph.add_edge("posts","intermediate")
graph.add_edge("feedback","intermediate")
'''
graph.add_edge("gen_insights","content")
graph.add_edge("posts","feedback")
graph.add_edge("feedback",END)'''

def dummy_func_for_intermediate_node(state:AgentState):
    return {"messages":state['messages']}
graph.add_node("intermediate",dummy_func_for_intermediate_node)
def decide_intermediate_step(state:AgentState):
    with open("data/user_ques.txt",'r') as f:
        request = f.read()
    res = decide_intermediate_step_using_msg(request,state['messages'][-1])
    if res == '0':
        return "insights"
    if res == '1':
        return "gen-content"
    if res == '3':
        return "posts"
    
    if res == "4":
        return "feedback"
    else:
        return "END"
graph.add_conditional_edges(
    "intermediate",
    decide_intermediate_step,
    {
        
        "gen-content":"content",
        "insights":"gen_insights",
        "design":"design",
        "posts":"posts",
        "feedback":"feedback",
        "END":END
    }
    
)
graph.add_edge("content","intermediate")
graph.add_edge("gen_insights","intermediate")
graph.add_edge("design","intermediate")
graph.add_edge("posts","intermediate")
graph.add_edge("feedback","intermediate")
app = graph.compile()
user_inp = input("User: ")
conversational_history = []
if __name__ == "__main__":

    while user_inp !='exit':
        conversational_history.append(HumanMessage(content=user_inp))
        result = app.invoke({"messages":conversational_history})
        conversational_history = result['messages']
        print("AI: ",dict(conversational_history[-1])['content'])
        user_inp = input("User: ")

