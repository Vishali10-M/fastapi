from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from pydantic import BaseSettings

class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017"

    class Config:
        env_file = ".env"

settings = Settings()

def get_database():
    client = AsyncIOMotorClient(settings.mongodb_url)
    return client.get_database()

database = get_database()
