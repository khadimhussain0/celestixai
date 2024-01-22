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
async def create_model(
    model_metadata: ModelConstellationCreate = Depends(ModelConstellationCreate.as_form),
    model_file: UploadFile = File(...),
    icon_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    model_uuid = str(uuid.uuid4())
    icon_uuid = str(uuid.uuid4())
    model_path = os.path.join(FILE_STORAGE_PATH, model_file.filename + "." + model_uuid)
    icon_path = os.path.join(FILE_STORAGE_PATH, icon_file.filename + "." + icon_uuid)

    async with open(model_path, "wb") as f:
        await f.write(model_file.file.read())
    async with open(icon_path, "wb") as f:
        await f.write(icon_file.file.read())

    model_db = ModelConstellation(
        uuid=model_uuid,
        model_name=model_metadata.model_name,
        icon_uuid=icon_uuid,
        icon_filename=icon_file.filename,
        filename=model_file.filename,
        file_size=os.path.getsize(model_path),
        parameters=model_metadata.parameters,
        model_class=model_metadata.model_class,
        model_task=model_metadata.model_task,
    )
    db.add(model_db)
    await db.commit()
    await db.refresh(model_db)

    return model_db


@router.get("/", response_model=List[ModelConstellationRead])
async def get_model_constellation(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    models_constellation = await db.query(ModelConstellation).all()

    if len(models_constellation) == 0:
        raise HTTPException(status_code=404, detail="Model not found")

    return models_constellation
