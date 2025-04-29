# Tractor Company Customer Support Chatbot

A modern customer support chatbot built using LangChain, LangGraph, and Streamlit for a tractor company. The chatbot provides an interactive web interface for handling customer inquiries about tractors, maintenance, and general support.

## Features

- 🚜 Interactive web interface powered by Streamlit
- 💬 Real-time chat with AI-powered responses
- 📱 Responsive design that works on desktop and mobile
- 📚 Comprehensive knowledge base of sample tractor information
- 🔄 Chat history persistence during session
- ℹ️ Sidebar with tractor model specifications and information
- 🤖 AI-powered responses using LangChain and LangGraph
- ⚡ Fast and efficient query processing

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

4. Run the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## Project Structure

- `app.py`: Streamlit web interface implementation
- `chatbot.py`: Core chatbot logic using LangChain and LangGraph
- `knowledge_base.py`: Structured data containing tractor information
- `requirements.txt`: Project dependencies
- `.env`: Environment variables (not tracked in git)

## Knowledge Base

The chatbot's knowledge base (`knowledge_base.py`) contains structured information about:
- Tractor models and specifications
- Maintenance schedules
- Common issues and troubleshooting
- Company information and contact details

## Usage

1. Open the web interface in your browser
2. Type your question in the chat input at the bottom
3. View the response from the chatbot
4. Use the sidebar to browse available tractor models and specifications
5. Chat history is maintained during your session

## Development

To modify the chatbot:
- Edit `knowledge_base.py` to update the information database
- Modify `chatbot.py` to change the core logic
- Update `app.py` to modify the web interface

## Dependencies

- streamlit==1.32.0
- langchain==0.1.0
- langgraph==0.0.15
- python-dotenv==1.0.0
- openai==1.12.0
- pydantic==2.5.2 