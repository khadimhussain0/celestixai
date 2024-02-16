from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.models import Model
from app.core.config import LLM_ENGINE_URL, FILE_STORAGE_PATH
import httpx  # for making HTTP requests
from uuid import uuid4

router = APIRouter(
    prefix="/deploy",
    tags=["Deployments"]
)


async def send_deployment_request(payload):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        print(LLM_ENGINE_URL + "/create")
        response = await client.post(LLM_ENGINE_URL + "/create", json=payload, timeout=60.0)
        return response


@router.post("/")
async def create_model(
    model_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    model = db.query(Model).filter(Model.id == model_id, current_user.id == Model.user_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    model_path = f"{FILE_STORAGE_PATH}/{model.filename}.{model.uuid}"
    print(model_path)

    payload = {
        "model_path": model_path,
        "model": model.model_name
    }

    try:
        response = await send_deployment_request(payload)
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc)) from exc

    model.deploy = True
    db.commit()
    return {"message": "Deployment successful"}
