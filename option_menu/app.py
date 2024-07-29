import streamlit as st
import openai

# Load secrets
client_id = st.secrets["openai"]["client_id"]
client_secret = st.secrets["openai"]["client_secret"]
app_key = st.secrets["openai"]["app_key"]

# Initialize OpenAI client
openai.api_key = app_key

# Use these variables to connect to the OpenAI model
from streamlit_extras.stylable_container import stylable_container

pg = st.navigation([st.Page("1_Plotting_Demo.py"), st.Page("2_Mapping_Demo.py"), st.Page("3_DataFrame_Demo.py")])
pg.run()

# Function to create a stylable container
def stylable_container(css_styles):
    container = st.container()
    with container:
        st.markdown(
            f'<div style="{css_styles}">',
            unsafe_allow_html=True,
        )
    return container

# Define the CSS styles
css_styles = """
    border: 1px solid rgba(49, 51, 63, 0.2);
    border-radius: 0.5rem;
    padding: calc(1em - 1px);
"""

# Function to handle the AI response
def get_ai_response(user_input):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_input,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Layout for sidebar chat
user_input = st.text_input("Enter your query:")
if user_input:
    ai_response = get_ai_response(user_input)
    st.write(ai_response)

# Function to handle the AI response (mockup)
def get_ai_response(user_input):
    return f"AI Response to: {user_input}"

# Layout for sidebar chat
def sidebar_chat():
    st.sidebar.header("Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display messages
    for message in st.session_state.messages:
        with st.sidebar:
            with stylable_container(css_styles):
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    # Always place the input field at the bottom
    with st.sidebar:
        with stylable_container(css_styles):
            st.write("")  # This ensures the input field is at the bottom
            prompt = st.chat_input("What is up?")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.sidebar:
            with st.chat_message("user"):
                st.markdown(prompt)

        with st.sidebar:
            with stylable_container(css_styles):
                with st.chat_message("assistant"):
                    stream = client.chat.completions.create(
                        model=st.session_state["openai_model"],
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                        stream=True,
                    )
                    response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "content": response})

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Run the sidebar chat
sidebar_chat()