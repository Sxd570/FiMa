from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://fima:Fima1234!@localhost:27017/fima?authSource=admin")
db = client["fima"]

test_message = {
    "message_id": "msg1",
    "conversation_id": "conversaton123",
    "user_id": "be2323eb-38ac-5a90-85a3-26b6f4fdfb25",
    "sender": "user",
    "content_type": "text",
    "content": "Hello, this is a test message.",
    "created_at": datetime.utcnow(),
    "metadata": {
        "token_used": 10,
        "model": "test-model",
        "temperature": 0.5
    }
}

db["conversations"].insert_one(test_message)

# Add a response from agent
agent_message = {
    "message_id": "msg2",
    "conversation_id": "conversaton123",
    "user_id": "be2323eb-38ac-5a90-85a3-26b6f4fdfb25",
    "sender": "agent",
    "content_type": "text",
    "content": "Hi, I am the agent. How can I help you?",
    "created_at": datetime.utcnow(),
    "metadata": {
        "token_used": 12,
        "model": "test-model",
        "temperature": 0.5
    }
}

db["conversations"].insert_one(agent_message)
print("Test messages inserted.")
