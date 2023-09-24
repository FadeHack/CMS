import openai
import json
from indexing import index
import os 
os.environ["OPENAI_API_KEY"] = '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'


class Chatbot:
    def __init__(self, api_key, index):
        self.index = index
        openai.api_key = api_key
        self.chat_history = []

    def generate_response(self, user_input):
        prompt = "\n".join([f"{message['role']}: {message['content']}" 
                           for message in self.chat_history[-5:]])
        prompt += f"\nUser: {user_input}"
        query_engine = index.as_query_engine()
        response = query_engine.query(user_input)

        message = {"role": "assistant", "content": response.response}
        self.chat_history.append({"role": "user", "content": user_input})
        self.chat_history.append(message)
        return message

    def load_chat_history(self, filename):
        try:
            with open(filename, 'r') as f:
                self.chat_history = json.load(f)
        except FileNotFoundError:
            pass

    def save_chat_history(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.chat_history, f)

api_key = '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'
index_instance =  index

chatbot_instance = Chatbot(api_key=api_key, index=index_instance)