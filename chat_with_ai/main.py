#!/usr/bin/env python3
from langchain_openai import ChatOpenAI
from log_callback_handler import NiceGuiLogElementCallbackHandler
import os
import requests
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
import base64

from nicegui import ui

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


@ui.page('/')
def main():
    llm = init_llm()

    async def send() -> None:
        question = text.value
        text.value = ''

        with message_container:
            ui.chat_message(text=question, name='You', sent=True)
            response_message = ui.chat_message(name='Bot', sent=False)
            spinner = ui.spinner(type='dots')

        response = ''
        async for chunk in llm.astream(question, config={'callbacks': [NiceGuiLogElementCallbackHandler(log)]}):
            response += chunk.content
            response_message.clear()
            with response_message:
                ui.html(response)
            ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
        message_container.remove(spinner)

    ui.add_css(r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}')

    # the queries below are used to expand the contend down to the footer (content can then use flex-grow to expand)
    ui.query('.q-page').classes('flex')
    ui.query('.nicegui-content').classes('w-full')

    with ui.tabs().classes('w-full') as tabs:
        chat_tab = ui.tab('Chat')
        logs_tab = ui.tab('Logs')
    with ui.tab_panels(tabs, value=chat_tab).classes('w-full max-w-2xl mx-auto flex-grow items-stretch'):
        message_container = ui.tab_panel(chat_tab).classes('items-stretch')
        with ui.tab_panel(logs_tab):
            log = ui.log().classes('w-full h-full')

    with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
        with ui.row().classes('w-full no-wrap items-center'):
            placeholder = 'type a prompt'
            text = ui.input(placeholder=placeholder).props('rounded outlined input-class=mx-3') \
                .classes('w-full self-center').on('keydown.enter', send)
        ui.markdown('not original') \
            .classes('text-xs self-end mr-8 m-[-1em] text-primary')


ui.run(title='Chat with GPT-3 (example)')
