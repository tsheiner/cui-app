import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Streamlit! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)

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