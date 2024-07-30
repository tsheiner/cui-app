# app.py
import streamlit as st
from streamlit_option_menu import option_menu
from options.plotting import plotting
from options.dataframe import dataframe
import requests
import base64
import os
import requests
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from streamlit_extras.bottom_container import bottom
import streamlit.components.v1 as components

# Create the option menu
selected = option_menu(
    menu_title="Main Menu",  # Add the menu_title argument
    options=["Plotting", "DataFrame"],
    icons=["", ""],
    menu_icon="",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"},
        #"icon": {"color": "orange", "font-size": "25px"},
        "icon": {"display": "none"},
        "nav-link": {
            "font-size": "25px",
            "text-align": "left",
            "margin": "0px",
            "--hover-color": "#eee"
        },
        "nav-link-selected": {"background-color": "blue"},
        "menu-title": {"display": "none"},
        "menu hr": {"display": "none"},
        "hr": {"display": "none"}
    },
)

# Navigate to the selected page
if selected == "Plotting":
    plotting()
elif selected == "DataFrame":
    dataframe()

# Load environment variables
load_dotenv()

# Function to get an authentication token
def azure_ai_token():
    url = "https://id.cisco.com/oauth2/default/v1/token"

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    payload = "grant_type=client_credentials"
    value = base64.b64encode(f'{client_id}:{client_secret}'.encode('utf-8')).decode('utf-8')
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {value}"
    }

    token_response = requests.request("POST", url, headers=headers, data=payload)
    API_KEY = token_response.json()["access_token"]
    return API_KEY

# Function to initialize the LLM
def init_llm():
    user_info = '{"appkey": "' + os.getenv('APP_KEY') + '"}'
    llm = AzureChatOpenAI(
        azure_endpoint='https://chat-ai.cisco.com',
        openai_api_version="2023-08-01-preview",
        deployment_name='gpt-35-turbo',
        openai_api_key=azure_ai_token(),
        openai_api_type='azure',
        model_kwargs={'user': user_info}
    )
    return llm

# Function to send a prompt to the LLM
def send_prompt(prompt):
    llm = init_llm()
    response = llm.invoke(prompt)
    return response.content

# Inject custom CSS
# st.markdown("""
#     <style>
#     .sidebar .sidebar-content {
#         display: flex;
#         flex-direction: column;
#         height: 100%;
#     }
#     .sidebar .sidebar-content .chat-history {
#         flex-grow: 1;
#         overflow-y: auto;
#     }
#     .sidebar .sidebar-content .chat-input {
#         position: sticky;
#         bottom: 0;
#         background-color: #f0f2f6;
#         padding: 10px 0;
#     }
#     </style>
#     <script>
#     document.addEventListener('DOMContentLoaded', function() {
#         var chatInput = document.querySelector('.chat-input');
#         var observer = new MutationObserver(function() {
#             chatInput.scrollIntoView({ behavior: 'smooth', block: 'end' });
#         });
#         observer.observe(document.querySelector('.chat-history'), { childList: true });
#     });
#     </script>
#     """, unsafe_allow_html=True)

# Main logic
st.sidebar.title("Chat with AI")

# Initialize session state for chat history and input
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = ""
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# Function to handle user input
def handle_input():
    user_input = st.session_state.user_input
    if user_input:
        response = send_prompt(user_input)
        if response:
            # Update chat history
            st.session_state.chat_history += f"User: {user_input}\n\nAI: {response}\n\n"
            # Clear the input box
            st.session_state.user_input = ""
            #st.rerun()
        else:
            st.sidebar.error("Failed to get a response from the AI.")

# # Display chat history
# st.sidebar.markdown(body=st.session_state.chat_history)

# # Get user input with on_change callback
# st.sidebar.text_input("Enter your message:", value=st.session_state.user_input, key="user_input", on_change=handle_input)

 
# with bottom():
#         st.write("This is the bottom container")
#         st.text_input("This is a text input in the bottom container")

# Sidebar layout

with st.sidebar:
    with st.expander("Chat History", expanded=True):
        st.markdown(st.session_state.chat_history)
    
    st.text_input("Enter your message:", value=st.session_state.user_input, key="user_input", on_change=handle_input)

# Inject JavaScript to assign a custom class to the text input
components.html("""
     <script>
    document.addEventListener('DOMContentLoaded', function() {
        var textInput = parent.document.querySelectorAll('input[type="text"]');
        if (textInput.length > 0) {
            textInput[0].classList.add('chatInput');
        }
    });
    </script>
""")

st.markdown(
    """
    <style>
    .chatInput {
        border: 2px solid #4CAF50;
        padding: 10px;
        font-size: 16px;
        position: sticky;
        bottom: 0; /* Stick to the bottom of the sidebar */
        width: calc(100% - 40px); /* Adjust width to fit within the sidebar */
    }
    </style>
    """,
    unsafe_allow_html=True
)