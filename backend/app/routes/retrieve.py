from fastapi import APIRouter
from app.db.metadata import engine, mongo_db
import os, json
from app.core.config import LOCAL_STORAGE_PATH
from app.db.redis_client import redis_client
import re

router = APIRouter()

def sanitize_email(email: str) -> str:
    """Convert email to a safe string for table/collection/folder names."""
    return re.sub(r'\W|^(?=\d)', '_', email)

@router.get("/retrieve/json/{email}")
def retrieve_json(email: str):
    key_safe = sanitize_email(email)
    cache_key = f"json:{key_safe}"
    cached = redis_client.get(cache_key)
    if cached:
        return {"cached": True, "data": json.loads(cached)}

    collection_name = f"user_{key_safe}_documents"
    if collection_name in mongo_db.list_collection_names():
        data = list(mongo_db[collection_name].find({}, {"_id":0}))
        redis_client.set(cache_key, json.dumps(data), ex=60)
        return {"cached": False, "db": "mongodb", "data": data}

    return {"db": None, "data": []}

@router.get("/retrieve/media/{email}")
def retrieve_media(email: str):
    key_safe = sanitize_email(email)
    user_folder = os.path.join(LOCAL_STORAGE_PATH, key_safe)
    if os.path.exists(user_folder):
        files = os.listdir(user_folder)
        return {"files": files}
    return {"files": []}
