import os
import json
from openai import OpenAI
from dotenv import load_dotenv

HISTORY_FILE = "chat_history.json"

class ChatManager:
    # Intialise the OpenAI client(checks the api key) and the chat history, loads the history
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.history = []
        self.history.append({"role": "system","content": (
                    "You're AlexAI. You are really unconfident"
                    "You're stuttering and mumbling, and you don't know what you're talking about. "
                    "You constantly make mistakes, like 2+2 =3, OOP is open opera progtress etc."
                    "And you're VERY lazy, and you don't want to do anything. "
                    "Goof around and be silly, and don't take anything seriously. "
                    )})
        self.load_history()
    
    #Check if this file exists, if it does, load the history from it, if something goes wrong, create a new history
    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r") as f:
                    loaded_history = json.load(f)
                    # Filter out any pre-existing system message to avoid duplication
                    non_system_msgs = [msg for msg in loaded_history if msg["role"] != "system"]
                    self.history.extend(non_system_msgs)
            except json.JSONDecodeError:
                self.history = []
        else:
            self.history = []

    # Converts the self.history in JSON format
    def save_history(self):
        with open(HISTORY_FILE, "w") as f:
            json.dump(self.history, f, indent=2)

    # Adds a message, which contains the role and the content, to the history and saves it
    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})
        self.save_history()


    # Adds question to the history, calls ChatGPT 4o model, passes the history of chat to it, retrivies response, adds it to the history, and returns it
    def chat(self, user_input):
        self.add_message("user", user_input)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o" \
                "",
                messages=self.history
            )
            assistant_reply = response.choices[0].message.content
            self.add_message("assistant", assistant_reply)
            return assistant_reply
        except Exception as e:
            return f"Error: {str(e)}"