import requests
from datetime import datetime
import json
import uuid

class SinopsisAI:
    def __init__(self, api_key, user=uuid.uuid4().hex, session_id=uuid.uuid4().hex, conversation_id=uuid.uuid4().hex):
        self.api_key = api_key
        self.backend_url = 'https://sinopsis-ai-api-9739a6f1a007.herokuapp.com'
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.session = {
            "chat_history": [],
            "user": user,  
            "session_id": session_id,
            "conversation_id": conversation_id 
        }
        self._retrieve_existing_chat_history()

    def _retrieve_existing_chat_history(self):
        response = requests.post(f'{self.backend_url}/retrieve_chat_history', json={
            'conversation_id': self.session['conversation_id'],
            'api_key': self.api_key
        })
        
        if response.status_code == 200:
            self.session['chat_history'] = response.json()
        else:
            self.session['chat_history'] = []

    def update_conversation_in_db(self):
        response = requests.post(f'{self.backend_url}/update_conversation_in_db', json={
            'api_key': self.api_key,
            'session': self.session
        })

        if response.status_code != 200:
            print("Error updating conversation in database")
     
    def log_prompt(self, user_input):
        timestamp = datetime.utcnow().isoformat()
        self.session['chat_history'].append({
            "role": "User",
            "user": self.session['user'],
            "message": user_input,
            "timestamp": timestamp
        })
        self.update_conversation_in_db()

    def log_response(self, assistant_response, chatbot_name, model_name, model_input):
        timestamp = datetime.utcnow().isoformat()
        input_string = json.dumps(model_input)
        self.session['chat_history'].append({
            "role": "Assistant",
            "message": assistant_response,
            "timestamp": timestamp,
            "chatbot_name": chatbot_name,
            "model_name": model_name,
            "model_input": input_string
        })
        self.update_conversation_in_db()