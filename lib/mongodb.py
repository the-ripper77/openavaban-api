import os
from pymongo import MongoClient
from pymongo.collection import Collection


_client = None
_db = None


def get_client() -> MongoClient:
    global _client
    if _client is None:
        uri = os.getenv("MONGODB_URI")
        if not uri:
            raise ValueError("MONGODB_URI not set")
        _client = MongoClient(uri, serverSelectionTimeoutMS=5000, connectTimeoutMS=5000)
    return _client


def get_db(database: str = "openavaban"):
    global _db
    if _db is None:
        _db = get_client()[database]
    return _db


def get_collection(collection: str = "profiles", database: str = "openavaban") -> Collection:
    return get_db(database)[collection]
