import os, re
from sqlalchemy import Table, Column, Integer, String, MetaData
from app.db.metadata import engine, metadata
from app.utils.file_utils import ensure_storage_path, get_file_extension
from app.db.minio_client import minio_client
from app.core.config import MINIO_BUCKET, LOCAL_STORAGE_PATH

ensure_storage_path(LOCAL_STORAGE_PATH)

def sanitize_email(email: str) -> str:
    return re.sub(r'\W|^(?=\d)', '_', email)

def handle_media_upload(email: str, file_name: str, file_bytes: bytes):
    key_safe = sanitize_email(email)

    # Save locally
    user_folder = os.path.join(LOCAL_STORAGE_PATH, key_safe)
    os.makedirs(user_folder, exist_ok=True)
    file_path = os.path.join(user_folder, file_name)
    with open(file_path, "wb") as f:
        f.write(file_bytes)

    # Upload to MinIO
    minio_client.fput_object(MINIO_BUCKET, f"{key_safe}/{file_name}", file_path)

    # Save metadata in Postgres
    table_name = f"user_{key_safe}_media"
    if not engine.dialect.has_table(engine, table_name):
        table = Table(
            table_name, metadata,
            Column("id", Integer, primary_key=True),
            Column("file_name", String),
            Column("file_path", String),
            Column("file_type", String)
        )
        table.create(engine)
    else:
        table = Table(table_name, metadata, autoload_with=engine)

    file_ext = get_file_extension(file_name)
    with engine.connect() as conn:
        conn.execute(table.insert(), [{"file_name": file_name, "file_path": file_path, "file_type": file_ext}])

    return {"file_name": file_name, "file_type": file_ext, "local_path": file_path}
