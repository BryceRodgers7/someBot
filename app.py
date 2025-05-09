import streamlit as st
from chatbot_core import create_chatbot
from knowledge_base import TRACTOR_KNOWLEDGE

# Create the chatbot application
app = create_chatbot()

# Set page config
st.set_page_config(
    page_title="Tractor Company Customer Support",
    page_icon="🚜",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stTextInput>div>div>input {
        background-color: #f0f2f6;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #2b313e;
        color: white;
    }
    .chat-message.bot {
        background-color: #f0f2f6;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.title("🚜 Tractor Company Customer Support")
st.markdown("Welcome to our customer support chatbot! How can I help you today?")

# Sidebar with information
with st.sidebar:
    st.header("About")
    st.markdown("""
    This chatbot can help you with:
    - Tractor models and specifications
    - Maintenance schedules
    - Common issues and troubleshooting
    - Company information
    """)
    
    st.header("Available Models")
    for model, info in TRACTOR_KNOWLEDGE["models"].items():
        st.subheader(model)
        st.write(info["description"])
        st.write("Specifications:")
        for spec, value in info["specifications"].items():
            st.write(f"- {spec.replace('_', ' ').title()}: {value}")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = app.invoke({"query": prompt})
                response = result.get("response", "I apologize, but I couldn't process your request.")
                st.markdown(response)
                
                # Add bot response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.session_state.messages.append({"role": "assistant", "content": "I apologize, but I encountered an error. Please try again."}) 