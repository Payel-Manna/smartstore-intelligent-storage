from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel, EmailStr
from app.services.json_processor import handle_json_upload
from app.services.media_processor import handle_media_upload

router = APIRouter()

class JSONRequest(BaseModel):
    email: EmailStr
    data: dict

@router.post("/upload/json")
def upload_json(payload: JSONRequest):
    result = handle_json_upload(payload.email, payload.data)
    return {"status": "ok", "details": result}

@router.post("/upload/media")
async def upload_media(email: EmailStr = Form(...), file: UploadFile = File(...)):
    file_bytes = await file.read()
    result = handle_media_upload(email, file.filename, file_bytes)
    return {"status": "ok", "details": result}
