from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Query
import uvicorn
import shutil
import os

from data_access.database import Base, engine
from data_access.repository import SqlAlchemyRepository
from data_access.csv_reader import CsvReader
from business.import_service import ImportService, ImportValidationError
from business.import_controller import ImportController
from generator.csv_generator import CsvGenerator

csv_path = "generator/hotels.csv"

app = FastAPI(
    title="Hotel Data API",
    version="1.0.0"
)

def get_repo():
    repo = SqlAlchemyRepository()
    try:
        yield repo
    finally:
        repo.close()

@app.post("/generate-csv", summary="Generate CSV file", tags=["Controls"])
def generate_csv(delimiter: str = Query(",", description="The character used to separate CSV fields")):
    try:
        generator = CsvGenerator(path=csv_path, delimiter=delimiter)
        generator.generate()
        return {"status": "success", "message": "CSV file successfully generated"}
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Failed CSV generation: {err}")

@app.post("/import-data", summary="Import data from CSV to db", tags=["Controls"])
def import_data(repo: SqlAlchemyRepository = Depends(get_repo)):
    Base.metadata.create_all(bind=engine)

    csv_reader = CsvReader()
    service = ImportService(csv_reader=csv_reader, repository=repo)
    controller = ImportController(import_service=service)

    try:
        controller.start_import(csv_path)
        return {"status":"success", "message": f"Data from {csv_path} successfully imported"}
    except ImportValidationError as err:
        raise HTTPException(status_code=400, detail=f"Import Validation Error: {err}")
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {err}")
    finally:
        repo.close()

@app.post("/import-data-from-csv", summary="Import data from uploaded CSV file to db", tags=["Controls"])
def import_data_from_uploaded_csv(
        file: UploadFile = File(...),
        repo: SqlAlchemyRepository = Depends(get_repo)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only .csv files are allowed.")
    
    temp_file_path = f"temp_{file.filename}"

    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as err:
        raise HTTPException(status_code=500, detail="Failed to save uploaded file: {err}")
    
    Base.metadata.create_all(bind=engine)
    csv_reader = CsvReader()
    service = ImportService(csv_reader=csv_reader, repository=repo)
    controller = ImportController(import_service=service)

    try:
        controller.start_import(temp_file_path)
        return {"status": "success", "message": f"Successful import from {file.filename}"}
    except ImportValidationError as err:
        raise HTTPException(status_code=400, detail=f"Import Validation Error: {err}")
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {err}")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__ == '__main__':
    print("Starting API server... Access Swagger at http://127.0.0.1:8000/docs")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
