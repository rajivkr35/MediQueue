# backend/auth.py

from fastapi import APIRouter, HTTPException, Header, Request
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from dotenv import load_dotenv
from database import users_collection
from models import UserRegister, UserLogin
from auth_utils import verify_token
import os

# 📦 Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET", "your_super_secret_key")
JWT_EXPIRY_MINUTES = 60

# 🔐 Password hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🚀 FastAPI router
router = APIRouter()


# 🔐 JWT token creator
def create_token(email: str, role: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRY_MINUTES)
    payload = {
        "sub": email,
        "role": role,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


# ✅ Register Route
@router.post("/register")
async def register_user(user: UserRegister):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered.")

    hashed_password = pwd_context.hash(user.password)

    user_data = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "phone": user.phone,
        "role": user.role
    }

    if user.role == "patient":
        user_data.update({
            "age": user.age,
            "gender": user.gender,
            "address": user.address
        })
    elif user.role == "admin":
        user_data["hospital_name"] = user.hospital_name

    users_collection.insert_one(user_data)
    return {"message": "User registered successfully!"}


# ✅ Login Route
@router.post("/login")
def login_user(user: UserLogin):
    db_user = users_collection.find_one({"email": user.email})

    if not db_user or not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if db_user.get("role") != user.role:
        raise HTTPException(status_code=403, detail="Role mismatch")

    token = create_token(user.email, user.role)
    return {"access_token": token}


# ✅ Verify Route (returns email, role, hospital name if admin)
@router.get("/verify")
def verify_user(request: Request, Authorization: str = Header(None)):
    email = verify_token(Authorization)
    user = users_collection.find_one({"email": email})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "email": user.get("email"),
        "role": user.get("role"),
        "hospital_name": user.get("hospital_name", "")  # blank if patient
    }
