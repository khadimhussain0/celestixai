import os
import shutil
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.dataset import Dataset
from app.core.config import FILE_STORAGE_PATH, VECTOR_FILE_STORAGE_PATH
from app.services.vectorstore import DocumentProcessor

router = APIRouter(
    prefix="/rag",
    tags=["Retrieval Augmented Generation"]
)


@router.post("/build-vector-store")
def build_document_vector_store(datasets: dict, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    dataset_ids = datasets.get('datasets', [])
    if not dataset_ids:
        raise HTTPException(status_code=400, detail="No dataset IDs provided")

    user_datasets = db.query(Dataset).filter(Dataset.owner_id == current_user.id, Dataset.id.in_(dataset_ids)).all()
    if not user_datasets:
        raise HTTPException(status_code=404, detail="No datasets found for the current user with the provided IDs")

    user_dir = os.path.join(VECTOR_FILE_STORAGE_PATH, str(current_user.id))
    os.makedirs(user_dir, exist_ok=True)

    source_documents_dir = os.path.join(user_dir, "source_documents")
    os.makedirs(source_documents_dir, exist_ok=True)

    persist_dir = os.path.join(user_dir, "db")
    os.makedirs(persist_dir, exist_ok=True)

    for dataset in user_datasets:
        dataset_path = os.path.join(FILE_STORAGE_PATH, dataset.filename + "." + dataset.uuid)
        destination_path = os.path.join(source_documents_dir, dataset.filename + "." + dataset.uuid)
        if not os.path.exists(destination_path):
            try:
                shutil.copy(dataset_path, destination_path)
            except FileNotFoundError:
                raise HTTPException(status_code=500, detail="Failed to copy dataset file")

    processor = DocumentProcessor(source_directory=source_documents_dir, persist_directory=persist_dir)
    processor.process_documents()

    return {"success": True}
