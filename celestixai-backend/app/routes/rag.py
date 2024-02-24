import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.dataset import Dataset
from app.core.config import FILE_STORAGE_PATH
from app.services.vectorstore import DocumentProcessor
from langchain_community.embeddings import OllamaEmbeddings

router = APIRouter(
    prefix="/rag",
    tags=["Retrieval Augmented Generation"]
)


@router.post("/build-vector-store")
async def build_document_vector_store(datasets: dict, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    dataset_ids = datasets.get('datasets', [])
    if not dataset_ids:
        raise HTTPException(status_code=400, detail="No dataset IDs provided")

    user_datasets = db.query(Dataset).filter(Dataset.owner_id == current_user.id, Dataset.id.in_(dataset_ids)).all()
    if not user_datasets:
        raise HTTPException(status_code=404, detail="No datasets found for the current user with the provided IDs")

    ollama_embedder= OllamaEmbeddings(base_url='http://celestixai-ollama-1:11434')
    rag_files = []
    for dataset in user_datasets:
        dataset_path = os.path.join(FILE_STORAGE_PATH, dataset.uuid +"____" + dataset.filename)
        print(dataset_path)
        rag_files.append(dataset_path)
    processor = DocumentProcessor(files=rag_files, ollama_embedder=ollama_embedder)
    await processor.process_documents(str(current_user.id))

    return {"success": True}
