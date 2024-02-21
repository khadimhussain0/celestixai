from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetRead
from app.core.config import FILE_STORAGE_PATH
from app.services.dataset import delete_st_dataset
import os
import uuid
from typing import List


router = APIRouter(
    prefix="/dataset",
    tags=["Dataset"]
)


@router.post("/", response_model=DatasetRead)
def create_dataset(
    dataset: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    dataset_uuid = str(uuid.uuid4())
    dataset_path = os.path.join(FILE_STORAGE_PATH, dataset.filename + "." + dataset_uuid)

    with open(dataset_path, "wb") as f:
        f.write(dataset.file.read())

    dataset_db = Dataset(
        owner_id=current_user.id,
        uuid=dataset_uuid,
        filename=dataset.filename,
        file_size=os.path.getsize(dataset_path)
    )
    db.add(dataset_db)
    db.commit()
    db.refresh(dataset_db)

    return dataset_db


@router.get("/", response_model=List[DatasetRead])
def get_datasets(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    datasets = db.query(Dataset).filter(Dataset.owner_id == current_user.id).all()
    if len(datasets) == 0:
        raise HTTPException(status_code=404, detail="Dataset not found")

    return datasets


@router.delete("/{dataset_id}", response_model=DatasetRead)
def delete_dataset(dataset_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_dataset = db.query(Dataset).filter(Dataset.id == dataset_id, Dataset.owner_id == current_user.id).first()
    if db_dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    db.delete(db_dataset)
    db.commit()

    # Delete dataset from storage
    delete_st_dataset(os.path.join(FILE_STORAGE_PATH, db_dataset.filename + " ." + db_dataset.uuid))

    return db_dataset
