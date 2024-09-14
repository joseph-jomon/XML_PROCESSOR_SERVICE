# app/main.py

from fastapi import FastAPI, File, UploadFile, HTTPException
import os
import zipfile
from app.xml_validator import validate_xml
from app.xml_parser import parse_xml_to_dataframe

app = FastAPI()

UPLOAD_DIR = "./uploads"

# Endpoint to accept files via REST API
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save the uploaded file
        file_location = f"{UPLOAD_DIR}/{file.filename}"
        with open(file_location, "wb+") as f:
            f.write(file.file.read())

        # Handle compressed file extraction
        if zipfile.is_zipfile(file_location):
            with zipfile.ZipFile(file_location, 'r') as zip_ref:
                zip_ref.extractall(UPLOAD_DIR)
            # Assume there's only one XML file inside the zip
            xml_file = [f for f in os.listdir(UPLOAD_DIR) if f.endswith('.xml')][0]
        else:
            xml_file = file.filename

        # Validate the XML file
        xml_file_path = f"{UPLOAD_DIR}/{xml_file}"
        if not validate_xml(xml_file_path):
            raise HTTPException(status_code=400, detail="Invalid XML file")

        # Parse the XML file into a Pandas DataFrame
        df = parse_xml_to_dataframe(xml_file_path)

        return {"message": "File processed successfully", "dataframe_head": df.head().to_dict()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
