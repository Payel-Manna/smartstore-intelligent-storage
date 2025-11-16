from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import Table, Column, Integer, String, insert
from app.db.metadata import engine, metadata, users_table

router = APIRouter()

class UserCreate(BaseModel):
    email: str

@router.post("/user/register")
def register_user(user: UserCreate):
    # Check if user exists
    conn = engine.connect()
    existing = conn.execute(users_table.select().where(users_table.c.email == user.email)).fetchone()
    if existing:
        conn.close()
        return {"status": "exists", "email": user.email}
    
    # Insert user
    conn.execute(users_table.insert().values(email=user.email))
    conn.close()
    return {"status": "ok", "email": user.email}
