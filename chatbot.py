from chatbot_core import create_chatbot

# Create the chatbot application
app = create_chatbot()

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