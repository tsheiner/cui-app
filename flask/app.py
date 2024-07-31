import os
import base64
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from flask import Flask, render_template

app = Flask(__name__)

# Function to get Azure AI token
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

    #url = "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"  # Replace with your tenant ID
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
    system_message = (
    "You are pretending to be a network management assistant. Pretend you have access to all the APIs for a large Meraki network."
    "You will provide made up information about clients, switches, and access points on the network. "
    "If a user asks about one of these topics, include a command to switch to the appropriate "
    "tab in your response. Use the following format at the end of your response: [SWITCH_TAB: <tab_name>], "
    "where <tab_name> is either Clients, Switches, or Access Points."
    "If you are including a command to switch to a tab, ONLY mention this in the end of your response."
)
    
    llm = init_llm()
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]
    response = llm.invoke(messages)
    return response.content

def parse_response(response):
    parts = response.split('[SWITCH_TAB:')
    if len(parts) > 1:
        tab_name = parts[1].split(']')[0].strip()
        clean_response = parts[0].strip()
        return clean_response, tab_name
    return response, None

# Endpoint to handle terminal shell requests
@app.route('/api/terminal', methods=['POST'])
def terminal():
    data = request.json
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    response = send_prompt(prompt)
    clean_response, tab_name = parse_response(response)
    return jsonify({"response": clean_response, "switch_tab": tab_name})


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tab/<int:tab_id>')
def tab(tab_id):
    titles = {1: 'Clients', 2: 'Switches', 3: 'Access Points'}
    return render_template(f'tab{tab_id}.html', title=titles.get(tab_id, f'Tab {tab_id}'))

if __name__ == '__main__':
    app.run(debug=True)