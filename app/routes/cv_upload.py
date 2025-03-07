from fastapi import APIRouter, UploadFile, File
from nlp.text_extractor import extract_text_from_pdf
from nlp.criteria_matching import match_criteria

router = APIRouter()


@router.post("/upload/")
async def upload_cv(file: UploadFile = File(...)):
    try:
        # Extract text from uploaded PDF
        contents = await file.read()
        text = extract_text_from_pdf(contents)

        # Get structured O-1A assessment
        assessment = match_criteria(text)

        return {"filename": file.filename, "assessment": assessment}

    except Exception as e:
        return {"error": str(e)}
