import uuid
import aiofiles
from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse

from app.service import count_frequency_stat


router = APIRouter(prefix="/public")


@router.post("/report/export")
async def get_report(file: UploadFile):
    extention = _get_extension(file.filename)
    if extention != "txt":
        return {"message": "Требуется файл с расширением .txt"}
    
    filepath = f"files/raw/{uuid.uuid4()}.txt"
    async with aiofiles.open(filepath, "wb") as f:
        while chunk := await file.read(1024 * 1024):
            await f.write(chunk)
    reportpath = await count_frequency_stat(filepath)

    return FileResponse(reportpath) 


def _get_extension(filename: str | None) -> str | None:
    if not filename:
        return None
    
    filename_parts = filename.split('.')
    if len(filename_parts) == 1:
        return None
    
    return filename_parts[-1]