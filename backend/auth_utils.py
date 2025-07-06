# backend/auth_utils.py

from fastapi import Header, HTTPException
from jose import jwt, JWTError
import os

SECRET_KEY = os.getenv("JWT_SECRET", "your_super_secret_key")

def verify_token(Authorization: str = Header(None)):
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = Authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
