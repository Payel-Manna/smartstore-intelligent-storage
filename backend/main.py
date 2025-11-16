from fastapi import FastAPI
from app.routes import upload, retrieve , user

app = FastAPI(title="Smart Multi-Modal Storage Backend")

# Include routes without version prefix
app.include_router(upload.router)
app.include_router(retrieve.router)
app.include_router(user.router)
