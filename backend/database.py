# backend/database.py

from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)

db = client["queue_system"]
users_collection = db["users"]

# ✅ Add this line
patients_collection = db["patients"]