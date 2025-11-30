# QA Chatbot Documentation

## Problem Statement

Users need an accessible and interactive interface to communicate with Google's Gemini AI models without directly working with API calls or command-line tools. The challenge is to create a user-friendly chatbot application that:

- Provides seamless interaction with Gemini AI models
- Maintains conversation history and context
- Allows users to save and retrieve past conversations
- Offers flexibility in choosing different AI models
- Handles API configuration securely
- Presents a clean, intuitive user interface

## Tech Stack

### Core Technologies
- **Streamlit** - Web application framework for creating the UI
- **Google Generative AI (genai)** - Official Google Gemini API client
- **Python 3.x** - Programming language
- **python-dotenv** - Environment variable management

### Python Libraries
- `streamlit` - Frontend framework
- `google-generativeai` - Gemini API integration
- `datetime` - Timestamp generation
- `json` - Chat log serialization
- `os` - File system operations
- `dotenv` - Environment configuration

## Application Architecture

### File Structure
```
project/
├── app.py                 # Main application file
├── .env                   # Environment variables (API key)
├── requirements.txt       # Python dependencies
└── chat_logs/            # Auto-generated chat storage
    └── chat_*.json       # Individual chat sessions
```

## Process Flow

### 1. Initialization Phase
- Load environment variables from `.env` file
- Configure Streamlit page settings (title, icon, layout)
- Initialize session state variables for messages and chat history

### 2. API Configuration
- Attempt to load API key from environment variable
- Fall back to manual input if environment variable not found
- Configure Gemini API client with the provided key

### 3. User Interaction Loop
- Display existing chat messages from session state
- Accept user input through chat interface
- Send user query to selected Gemini model
- Receive and display AI response
- Update session state with new messages

### 4. Chat Management
- Save conversations to JSON files with timestamps
- Load previous conversations from saved files
- Clear or start new chat sessions

## User Interface Components

### Main Chat Area
**Components:**
- **Title & Header** - Application branding and description
- **Chat Messages Display** - Scrollable conversation history
- **Chat Input Box** - User query input field
- **Message Bubbles** - Differentiated user/assistant messages

### Sidebar Configuration Panel

#### API Configuration Section
- **API Key Input** - Secure password field for manual entry
- **Status Indicator** - Shows if key is loaded from environment or manually entered
- **Help Text** - Guidance on setting environment variables

#### Model Selection
- **Dropdown Menu** - Choose between available Gemini models:
  - gemini-2.5-flash (Fast responses)
  - gemini-2.5-pro (Advanced reasoning)
  - gemini-2.0-flash (Balanced performance)

#### Chat Controls
- **Clear Chat Button** - Removes all messages from current session
- **New Chat Button** - Saves current chat and starts fresh session

#### Chat Logs Management
- **Save Current Chat** - Manually save ongoing conversation
- **Recent Chats Expander** - View and load last 5 saved conversations
- **Chat Counter** - Total number of saved conversations

## Step-by-Step Explanation

### Step 1: Environment Setup
```python
load_dotenv()
```
Loads the API key from a `.env` file to keep sensitive credentials secure and out of the codebase.

### Step 2: Page Configuration
```python
st.set_page_config(page_title="QA Chatbot", page_icon="🤖", layout="centered")
```
Configures the browser tab title, favicon, and page layout for optimal viewing.

### Step 3: Session State Initialization
```python
if 'messages' not in st.session_state:
    st.session_state.messages = []
```
Creates persistent storage for chat messages that survives between Streamlit reruns.

### Step 4: API Key Management
The application first checks for an environment variable, then falls back to manual input:
```python
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
```
This two-tier approach balances security with user convenience.

### Step 5: Chat Saving Function
```python
def save_chat_log(messages):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chat_logs/chat_{timestamp}.json"
```
Creates timestamped JSON files containing the full conversation history for later retrieval.

### Step 6: AI Response Generation
```python
def get_gemini_response(prompt, model_name):
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text
```
Instantiates the selected Gemini model and generates a response to the user's prompt.

### Step 7: Message Display Loop
```python
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
```
Iterates through stored messages and renders them with appropriate styling for user/assistant roles.

### Step 8: User Input Processing
```python
if prompt := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = get_gemini_response(prompt, model_name)
    st.session_state.messages.append({"role": "assistant", "content": response})
```
Captures user input, calls the AI model, and updates the conversation history.

### Step 9: Chat Loading
```python
def load_chat_log(filename):
    with open(filepath, 'r') as f:
        chat_data = json.load(f)
        st.session_state.messages = chat_data["messages"]
        st.rerun()
```
Loads a previously saved conversation and triggers a page refresh to display it.

### Step 10: Error Handling
Try-except blocks throughout the application catch and display errors gracefully:
- API connection failures
- Invalid API keys
- File read/write errors
- Model response errors

## Key Features

### 1. Persistent Chat History
Each conversation is stored in session state, maintaining context throughout the user's session.

### 2. Chat Archival System
Conversations are saved as JSON files with timestamps, allowing users to revisit previous discussions.

### 3. Model Flexibility
Users can switch between different Gemini models based on their needs (speed vs. capability).

### 4. Secure API Management
API keys can be stored in environment variables, keeping them out of the codebase and version control.

### 5. Intuitive UI/UX
Clean chat interface with clear visual distinction between user and AI messages.

## Usage Instructions

### First-Time Setup
1. Install required packages: `pip install -r requirements.txt`
2. Create a `.env` file with: `GEMINI_API_KEY=your_api_key_here`
3. Run the application: `streamlit run app.py`

### Using the Chatbot
1. Verify API key is loaded (check sidebar status)
2. Select preferred Gemini model
3. Type question in chat input box
4. View AI response in chat area
5. Continue conversation with follow-up questions

### Managing Conversations
- **Save**: Click "Save Current Chat" to preserve conversation
- **Load**: Expand "Recent Chats" and click on a saved chat
- **Clear**: Click "Clear Chat" to remove current messages
- **New Chat**: Click "New Chat" to save current and start fresh

## Benefits

- **User-Friendly**: No coding required to interact with Gemini API
- **Organized**: Automatic chat logging with timestamps
- **Flexible**: Multiple model options for different use cases
- **Secure**: Environment variable support for API credentials
- **Accessible**: Web-based interface accessible from any browser
- **Portable**: Self-contained application with minimal dependencies