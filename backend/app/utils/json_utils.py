import re
from sqlalchemy import Integer, Float, String, Boolean, JSON

# Flatten nested JSON (recursive)
def flatten_json(y, parent_key='', sep='_'):
    items = {}
    for k, v in y.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_json(v, new_key, sep=sep))
        elif isinstance(v, list):
            # Keep arrays as is for JSON/NoSQL or handle child tables for SQL
            items[new_key] = v
        else:
            items[new_key] = v
    return items

# Map Genson types → SQLAlchemy types
def map_genson_type_to_sql(schema_prop: dict, value):
    type_str = schema_prop.get("type", None)
    if type_str == "integer":
        return Integer
    elif type_str == "number":
        return Float
    elif type_str == "boolean":
        return Boolean
    elif type_str == "array":
        return JSON
    else:
        return String

# Classify JSON as SQL vs NoSQL
def classify_json(json_data):
    def depth(obj):
        if isinstance(obj, dict):
            return 1 + max([depth(v) for v in obj.values()] or [0])
        elif isinstance(obj, list):
            if len(obj) == 0:
                return 1
            return 1 + max([depth(i) for i in obj])
        else:
            return 0
    json_depth = depth(json_data)
    arrays = any(isinstance(v, list) for v in json_data.values())
    if json_depth <= 2 and not arrays:
        return "sql"
    return "nosql"
