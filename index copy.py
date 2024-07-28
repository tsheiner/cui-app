from openai import OpenAI
import streamlit as st

# Define pages
list_page = st.Page("list_page.py", title="List Items", icon="📋")
map_page = st.Page("map_page.py", title="Map Items", icon="🗺️")

# Set up navigation
pg = st.navigation([list_page, map_page])

# Set common page configuration if needed
st.set_page_config(page_title="My Multi-Page App", page_icon=":world_map:")

# Execute the current page
pg.run()

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
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Always place the input field at the bottom
    with st.sidebar:
        st.write("")  # This ensures the input field is at the bottom
        prompt = st.chat_input("What is up?")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.sidebar:
            with st.chat_message("user"):
                st.markdown(prompt)

        with st.sidebar:
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