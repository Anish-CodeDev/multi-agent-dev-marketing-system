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
from gemini import extract_topics_from_tweets,extract_from_prompt
from twitter import retrieve_tweets_by_query
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
        1 → Content Agent - drafts posts, blogs, GitHub updates.
        2 → Design Helper Agent - creates diagrams, visuals, infographics.
        3 → Distribution Agent - posts/schedules across GitHub, LinkedIn, Twitter.
        4 → Feedback Agent - analyzes engagement (stars, likes, comments).
                                                                      
        Return with the index of the agent selected
            """)
    response = llm.invoke([instruction] + state['messages'])
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
    return {"messages":"content"}
def gen_insights(state:AgentState):
    topic = extract_from_prompt(state['messages'])
    tweets = retrieve_tweets_by_query(topic)
    topics = extract_topics_from_tweets(topics)
    topics = eval(topics)
    with open("data/insights.txt",'a+') as f:
        for topic in topics:
            f.write(topic)

    return {"messages":"data/insights.txt"}
def gen_design(state:AgentState):
    return {"messages":"design"}
def posts(state:AgentState):
    return {"messages":"posts"}
def manage_feedback(state:AgentState):
    return {"messages":"feedback"}
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
graph.add_edge("gen_insights",END)
graph.add_edge("content",END)
graph.add_edge("design",END)
graph.add_edge("posts",END)
graph.add_edge("feedback",END)
app = graph.compile()

user_inp = input("User: ")
conversational_history = []
while user_inp !='exit':
    conversational_history.append(HumanMessage(content=user_inp))
    result = app.invoke({"messages":conversational_history})
    conversational_history = result['messages']
    print("AI: ",dict(conversational_history[-1])['content'])
    user_inp = input("User: ")