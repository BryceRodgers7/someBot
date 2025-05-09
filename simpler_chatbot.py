from langchain.agents import Tool
# from langchain.agents.agent_toolkits import create_python_agent
from langchain.tools import tool
from langchain.chat_models import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing import TypedDict

@tool
def simple_calculator(expression: str) -> str:
    """Evaluates a basic math expression (e.g., 2 + 2)."""
    try:
        return str(eval(expression))
    except:
        return "Error evaluating expression."


llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    openai_api_key="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"
)

# def question_node(state):
#     question = state["input"]
#     response = llm.predict(question)
#     return {"response": response, "input": question}

# def calc_node(state):
#     expression = state["input"]
#     answer = simple_calculator.run(expression)
#     return {"response": answer, "input": expression}

# Define state using TypedDict
class ChatState(TypedDict):
    input: str
    response: str

# 2. Define your nodes
def question_node(state: ChatState):
    question = state["input"]
    return {"input": question, "response": f"Q: {question}"}

def calc_node(state: ChatState):
    expr = state["input"]
    try:
        result = eval(expr)
        return {"input": expr, "response": str(result)}
    except Exception:
        return {"input": expr, "response": "Invalid expression"}

def router(state: ChatState) -> str:
    if any(op in state["input"] for op in "+-*/"):
        return "calc"
    return "ask"



# 3. Build the graph
graph = StateGraph(ChatState)

# graph.add_node("router", router)
graph.add_node("ask", question_node)
graph.add_node("calc", calc_node)
graph.add_conditional_edges("router", router, {
    "ask": "ask",
    "calc": "calc"
})

graph.set_entry_point("router")
graph.set_finish_point("ask")  # or "calc" depending on where you want to end

# 4. Compile
workflow = graph.compile()



print("Chatbot is ready. Type 'quit' to exit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    state = {"input": user_input}
    result = workflow.invoke(state)
    print("Bot:", result["response"])