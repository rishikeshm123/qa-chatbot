import streamlit as st
import google.generativeai as genai
from datetime import datetime
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure page
st.set_page_config(
    page_title="QA Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Function to save chat log
def save_chat_log(messages):
    """Save chat messages to a JSON file"""
    if not os.path.exists("chat_logs"):
        os.makedirs("chat_logs")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chat_logs/chat_{timestamp}.json"
    
    chat_data = {
        "timestamp": timestamp,
        "messages": messages
    }
    
    with open(filename, 'w') as f:
        json.dump(chat_data, f, indent=2)

# Function to load chat log
def load_chat_log(filename):
    """Load chat messages from a JSON file"""
    filepath = os.path.join("chat_logs", filename)
    
    try:
        with open(filepath, 'r') as f:
            chat_data = json.load(f)
            st.session_state.messages = chat_data["messages"]
            st.rerun()
    except Exception as e:
        st.error(f"Error loading chat: {e}")

# Function to get response from Gemini
def get_gemini_response(prompt, model_name):
    """Get response from Gemini API"""
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Sidebar configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    
    # API Key - Try to get from environment variable first
    api_key = os.getenv("GEMINI_API_KEY")
    
    if api_key:
        genai.configure(api_key=api_key)
        st.success("✅ API Key loaded from environment variable!")
    else:
        # Fallback to manual input if env variable not set
        api_key = st.text_input("Enter Gemini API Key:", type="password", 
                                help="Set GEMINI_API_KEY environment variable to avoid manual entry")
        
        if api_key:
            genai.configure(api_key=api_key)
            st.success("API Key configured!")
        else:
            st.warning("⚠️ Please set GEMINI_API_KEY environment variable or enter key above")
    
    st.markdown("---")
    
    # Model selection
    model_name = st.selectbox(
        "Select Model:",
        ["gemini-2.5-flash", "gemini-2.5-pro","gemini-2.0-flash"]
    )
    
    st.markdown("---")
    
    # Chat controls
    st.subheader("💬 Chat Controls")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    with col2:
        if st.button("➕ New Chat", use_container_width=True):
            # Save current chat before starting new
            if st.session_state.messages:
                save_chat_log(st.session_state.messages)
            st.session_state.messages = []
            st.rerun()
    
    st.markdown("---")
    
    # Chat logs
    st.subheader("📝 Chat Logs")
    
    if st.button("💾 Save Current Chat", use_container_width=True):
        if st.session_state.messages:
            save_chat_log(st.session_state.messages)
            st.success("Chat saved successfully!")
        else:
            st.warning("No messages to save!")
    
    # Display saved chats
    if os.path.exists("chat_logs"):
        log_files = sorted(os.listdir("chat_logs"), reverse=True)
        if log_files:
            st.write(f"Total saved chats: {len(log_files)}")
            
            # Show recent chats
            with st.expander("View Recent Chats"):
                for log_file in log_files[:5]:  # Show last 5
                    if st.button(log_file, key=log_file):
                        load_chat_log(log_file)

# Main UI
st.title("🤖 QA Chatbot")
st.markdown("Ask me anything! I'm powered by Google's Gemini AI.")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your question here..."):
    if not api_key:
        st.warning("⚠️ Please enter your Gemini API key in the sidebar!")
    else:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_gemini_response(prompt, model_name)
                st.markdown(response)
        
        # Add assistant response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <small>Built with Streamlit & Google Gemini API</small>
    </div>
    """,
    unsafe_allow_html=True
)