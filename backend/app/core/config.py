# Postgres running as Docker service "postgres"
POSTGRES_URL = "postgresql://postgres:postgres@postgres:5432/hackathon_db"

# MongoDB running as Docker service "mongo"
MONGO_URL = "mongodb://mongo:27017"
MONGO_DB = "hackathon_db"

# Redis
REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_DB = 0

# Local storage path inside container
LOCAL_STORAGE_PATH = "/app/storage/uploads"

# MinIO configuration
MINIO_ENDPOINT = "minio:9000"
MINIO_ACCESS_KEY = "minioaccess"
MINIO_SECRET_KEY = "miniosecret"
MINIO_BUCKET = "user-media"
