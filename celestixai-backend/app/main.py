from app.routes import dataset
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routes import user, login
from app.routes import model_constellation, models
from app.routes import chat
from app.core.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    lifespan=lifespan,
    title="CelestixAI",
    description="Your Data, Your Model, Unified AI Platform",
    summary="Train LLMs(Large Language Models) with ease using CelestixAI",
    version="0.0.1",)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend's actual URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(login.router)
app.include_router(dataset.router)
app.include_router(model_constellation.router)
app.include_router(models.router)
app.include_router(chat.router)
