from pymongo import MongoClient
from gridfs import GridFS
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))

db = client["document_assistant"]

# Collections
chats_collection = db["chats"]
messages_collection = db["messages"]
summaries_collection = db["summaries"]

# GridFS
fs = GridFS(db)

print("✅ Connected to MongoDB Atlas")
