import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
from knowledge_base import TRACTOR_KNOWLEDGE

__all__ = ['create_chatbot']

# Load environment variables
load_dotenv()

# Initialize the language model
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

# Define the system prompt
SYSTEM_PROMPT = """You are a helpful customer support agent for a tractor company. 
You have access to the following information about our tractors and services:
{knowledge_base}

Please provide accurate and helpful responses to customer inquiries. 
If you don't know the answer, please say so and offer to connect them with a human agent."""

# Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{input}")
])

# Define the processing chain
chain = prompt | llm | StrOutputParser()

# Define the state schema
class ChatState(TypedDict):
    messages: Sequence[str]
    current_response: str | None
    should_escalate: bool

def process_query(query: str) -> str:
    """Process the user query and generate a response."""
    # Get the initial response
    response = chain.invoke({
        "input": query,
        "knowledge_base": str(TRACTOR_KNOWLEDGE)
    })
    
    return response

def should_escalate(query: str, response: str) -> bool:
    """Determine if the query should be escalated to a human agent."""
    # Check both user query and AI response for escalation terms
    user_escalation_terms = [
        "escalate",
        "human agent",
        "representative",
        "talk to someone",
        "speak to someone",
        "real person",
        "live agent"
    ]

    ai_escalation_terms = ["escalate",
        "human agent"
    ]
    
    # Check user query
    if any(term in query.lower() for term in user_escalation_terms):
        return True
    
    # Check AI response
    if any(term in response.lower() for term in ai_escalation_terms):
        return True
    
    return False

def create_chatbot():
    """Create and return the chatbot application with langgraph integration."""
    # Create the graph
    workflow = StateGraph(ChatState)

    # Define the nodes
    def process_message(state: ChatState) -> ChatState:
        query = state["messages"][-1]
        response = process_query(query)
        state["current_response"] = response
        state["should_escalate"] = should_escalate(query, response)
        return state

    def escalate(state: ChatState) -> ChatState:
        if state["should_escalate"]:
            state["current_response"] += "\n\nI've escalated your query to a human agent. They will contact you shortly."
        return state

    # Add nodes to the graph
    workflow.add_node("process", process_message)
    workflow.add_node("escalate", escalate)

    # Define the edges
    workflow.add_edge("process", "escalate")
    workflow.add_edge("escalate", END)
    workflow.set_entry_point("process")

    # Compile the graph
    app = workflow.compile()

    return app 