# backend/database.py

from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://rajivkr035:rajivdb1234@mediqueue.fidlmim.mongodb.net/?retryWrites=true&w=majority&appName=MediQueue")
client = MongoClient(MONGO_URI)

db = client["queue_system"]
users_collection = db["users"]

# ✅ Add this line
patients_collection = db["patients"]