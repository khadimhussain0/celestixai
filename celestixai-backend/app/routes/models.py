from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.model_constellation import ModelConstellation
from app.models.models import Model
from app.schemas.models import ModelCreate, ModelRead, ModelUpdateParameters
from typing import List

router = APIRouter(
    prefix="/models",
    tags=["Models"]
)


@router.post("/", response_model=ModelRead)
async def create_model(
    model_constellation_id: ModelCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    model_constellation_id = model_constellation_id.dict()
    print(type(model_constellation_id))
    print(model_constellation_id.get("id"))
    model_constellation = await db.query(ModelConstellation).get(model_constellation_id.get("id"))
    print(model_constellation)

    if not model_constellation:
        raise HTTPException(status_code=404, detail="Model Constellation not found")

    model_db = Model(
        user_id=current_user.id,
        model_constellation_id=model_constellation_id.get("id"),
        fine_tuned_model_path=None,
        model_name=model_constellation.model_name,
        parameters=model_constellation.parameters
    )
    db.add(model_db)
    await db.commit()
    await db.refresh(model_db)

    return model_db


@router.get("/", response_model=List[ModelRead])
async def get_models(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    models = await (
        db.query(Model)
        .join(ModelConstellation, ModelConstellation.id == Model.model_constellation_id)
        .filter(Model.user_id == current_user.id)
        .all()
    )

    if len(models) == 0:
        raise HTTPException(status_code=404, detail="Model not found")

    return models


@router.put("/{model_id}", response_model=ModelRead)
async def update_model(
    model_id: int,
    model_update: ModelUpdateParameters,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    model_db = await db.query(Model).filter(Model.id == model_id, Model.user_id == current_user.id).first()

    if not model_db:
        raise HTTPException(status_code=404, detail="Model not found")

    if model_update.model_name:
        model_db.model_name = model_update.model_name

    await db.commit()
    await db.refresh(model_db)

    return model_db
