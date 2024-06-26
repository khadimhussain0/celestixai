import os
import uuid
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.model_constellation import ModelConstellation
from app.schemas.model_constellation import ModelConstellationCreate, ModelConstellationRead
from app.core.config import FILE_STORAGE_PATH
from typing import List

router = APIRouter(
    prefix="/model_constellation",
    tags=["Model Constellation"]
)


@router.post("/", response_model=ModelConstellationRead)
def create_model(
    model_metadata: ModelConstellationCreate = Depends(ModelConstellationCreate.as_form),
    model_file: UploadFile = File(...),
    icon_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    model_uuid = str(uuid.uuid4())
    icon_uuid = str(uuid.uuid4())
    model_path = os.path.join(FILE_STORAGE_PATH, model_uuid + "____" + model_file.filename )
    icon_path = os.path.join(FILE_STORAGE_PATH, icon_uuid + "____" + icon_file.filename)

    with open(model_path, "wb") as f:
        f.write(model_file.file.read())
    with open(icon_path, "wb") as f:
        f.write(icon_file.file.read())

    model_db = ModelConstellation(
        uuid=model_uuid,
        model_name=model_metadata.model_name,
        ollama_name=model_metadata.ollama_name,
        hf_id=model_metadata.hf_id,
        icon_uuid=icon_uuid,
        icon_filename=icon_file.filename,
        filename=model_file.filename,
        file_size=os.path.getsize(model_path),
        parameters=model_metadata.parameters,
        model_class=model_metadata.model_class,
        model_task=model_metadata.model_task,
        is_vision=model_metadata.is_vision
    )
    db.add(model_db)
    db.commit()
    db.refresh(model_db)

    return model_db


@router.get("/", response_model=List[ModelConstellationRead])
def get_model_constellation(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    models_constellation = db.query(ModelConstellation).all()

    if len(models_constellation) == 0:
        raise HTTPException(status_code=404, detail="Model not found")

    return models_constellation
