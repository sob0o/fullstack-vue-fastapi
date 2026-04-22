from pymongo import MongoClient
from app.core.config import settings


client = None
database = None


def connect_to_mongo():
    global client, database
    client = MongoClient(settings.mongodb_url)
    database = client[settings.mongodb_db]
    print("Connected to MongoDB")


def close_mongo_connection():
    global client
    if client:
        client.close()
        print("MongoDB connection closed")


def get_database():
    return database