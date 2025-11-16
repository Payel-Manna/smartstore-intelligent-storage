from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from pymongo import MongoClient
from app.core.config import POSTGRES_URL, MONGO_URL, MONGO_DB

# PostgreSQL
engine = create_engine(POSTGRES_URL)
metadata = MetaData()

# MongoDB
mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client[MONGO_DB]

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, unique=True, nullable=False)
)

# Track files per email
files_table = Table(
    "files",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("filename", String, nullable=False),
    Column("file_type", String, nullable=False),
    Column("email", String, nullable=False, index=True)  # email instead of owner_id
)

metadata.create_all(bind=engine)
