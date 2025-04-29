import os
from typing import Dict, List, Tuple, Any
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langgraph.graph import Graph
from knowledge_base import TRACTOR_KNOWLEDGE

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

# Define the graph nodes
def process_query(state: Dict[str, Any]) -> Dict[str, Any]:
    """Process the user query and generate a response."""
    query = state["query"]
    response = chain.invoke({
        "input": query,
        "knowledge_base": str(TRACTOR_KNOWLEDGE)
    })
    return {"response": response}

def should_escalate(state: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
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
    user_query = state["query"].lower()
    if any(term in user_query for term in user_escalation_terms):
        return True, state
    
    # Check AI response
    ai_response = state["response"].lower()
    if any(term in ai_response for term in ai_escalation_terms):
        return True, state
    
    return False, state

def escalate_to_human(state: Dict[str, Any]) -> Dict[str, Any]:
    """Handle escalation to human agent."""
    state["response"] += "\n\nI've escalated your query to a human agent. They will contact you shortly."
    return state

# Create the graph
workflow = Graph()

# Add nodes
workflow.add_node("process_query", process_query)
workflow.add_node("escalate_to_human", escalate_to_human)

# Add edges
workflow.add_edge("process_query", "should_escalate")
workflow.add_conditional_edges(
    "should_escalate",
    should_escalate,
    {
        True: "escalate_to_human",
        False: "end"
    }
)

# Set the entry point
workflow.set_entry_point("process_query")

# Compile the graph
app = workflow.compile()

def chat():
    """Main chat loop."""
    print("Welcome to the Tractor Company Customer Support Chatbot!")
    print("Type 'quit' to exit.")
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            print("Thank you for chatting with us. Goodbye!")
            break
        
        # Process the query through the graph
        result = app.invoke({"query": user_input})
        print(f"\nBot: {result['response']}")

if __name__ == "__main__":
    chat() 