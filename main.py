from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import List

app = FastAPI()

client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client.my_database 
users_collection = db.users

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 30


class User(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserInDB(User):
    hashed_password: str


def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


async def get_user_by_email(email: str):
    return await users_collection.find_one({"email": email})


@app.post("/register/")
async def register_user(user: User):
    existing_user = await get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already in use")
    
    hashed_password = hash_password(user.password)
    new_user = {
        "email": user.email,
        "name": user.name,
        "hashed_password": hashed_password,
        "created_on": datetime.utcnow()
    }
    
    await users_collection.insert_one(new_user)
    return {"msg": "User registered successfully!"}
