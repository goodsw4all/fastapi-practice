from importlib.resources import path
from fastapi import APIRouter, FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import shutil
import pytesseract

router = APIRouter(
    prefix='/ocr',
    tags=['OCR']
)


@router.post('')
def ocr(image: UploadFile = File(...)):
    filePath = 'txtfile'
    with open(filePath, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
    return pytesseract.image_to_string(filePath, lang='eng')
