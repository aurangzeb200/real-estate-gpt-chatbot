import os
from datetime import datetime

CONVERSATION_FILE = "conversation.txt"

def store_conversation(query: str, response: str):
    """
    Appends the user's query and the model's response to the conversation.txt file with timestamps.
    """
    with open(CONVERSATION_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat()}] User: {query}\n")
        f.write(f"[{datetime.now().isoformat()}] Model: {response}\n\n")
