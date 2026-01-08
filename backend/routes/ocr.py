from fastapi import APIRouter, UploadFile, File, HTTPException
from services.ocr import parse_nutrition_label

router = APIRouter()

@router.post("/scan")
async def scan_label(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG, PNG, and WebP are supported.")
    
    try:
        contents = await file.read()
        extracted_data = parse_nutrition_label(contents)
        return extracted_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
