from genson import SchemaBuilder
from sqlalchemy import Table, Column, Integer, MetaData, inspect
from app.db.metadata import engine, metadata, mongo_db
from app.utils.json_utils import flatten_json, map_genson_type_to_sql, classify_json
import re

def sanitize_email(email: str) -> str:
    return re.sub(r'\W|^(?=\d)', '_', email)

def handle_json_upload(email: str, json_data: dict):
    key_safe = sanitize_email(email)

    # 1️⃣ Classify SQL vs NoSQL
    classification = classify_json(json_data)

    # 2️⃣ Generate Genson schema
    builder = SchemaBuilder()
    builder.add_object(json_data)
    genson_schema = builder.to_schema()

    # 3️⃣ Flatten JSON
    flat_json = flatten_json(json_data)

    if classification == "sql":
        table_name = f"user_{key_safe}_data"
        inspector = inspect(engine)  # ✅ Use inspector to check table existence

        if not inspector.has_table(table_name):
            columns = [Column("id", Integer, primary_key=True)]
            for k, v in flat_json.items():
                k_clean = re.sub(r'\W|^(?=\d)', '_', k)
                schema_prop = genson_schema.get("properties", {}).get(k, {})
                col_type = map_genson_type_to_sql(schema_prop, v)
                columns.append(Column(k_clean, col_type))

            table = Table(table_name, metadata, *columns)
            table.create(engine)
        else:
            table = Table(table_name, metadata, autoload_with=engine)

        # Insert flattened data
        insert_data = {re.sub(r'\W|^(?=\d)', '_', k): v for k, v in flat_json.items()}
        with engine.connect() as conn:
            conn.execute(table.insert(), [insert_data])
        return {"db": "postgresql", "table": table_name}

    else:
        # NoSQL
        collection_name = f"user_{key_safe}_documents"
        collection = mongo_db[collection_name]
        collection.insert_one(flat_json)
        return {"db": "mongodb", "collection": collection_name}
