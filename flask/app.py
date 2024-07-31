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
    llm = init_llm()
    response = llm.invoke(prompt)
    return response.content

# Endpoint to handle terminal shell requests
@app.route('/api/terminal', methods=['POST'])
def terminal():
    data = request.json
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    response = send_prompt(prompt)
    return jsonify({"response": response})

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/tab/<int:tab_id>')
# def tab(tab_id):
#     return render_template(f'tab{tab_id}.html', title=f'Tab {tab_id}')

@app.route('/tab/<int:tab_id>')
def tab(tab_id):
    titles = {1: 'Clients', 2: 'Switches', 3: 'Access Points'}
    return render_template(f'tab{tab_id}.html', title=titles.get(tab_id, f'Tab {tab_id}'))

if __name__ == '__main__':
    app.run(debug=True)