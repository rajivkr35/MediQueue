# backend/models.py

from pydantic import BaseModel, EmailStr
from typing import Optional, Literal

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None  # 👈 Make it optional
    role: Literal["patient", "admin"]
    
    # Patient-only fields
    age: Optional[int] = None
    gender: Optional[str] = None
    address: Optional[str] = None

    # Admin-only field
    hospital_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    role: Literal["admin", "patient"]