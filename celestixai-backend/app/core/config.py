import os
from datetime import timedelta

SECRET_KEY = "supersecritkey"
ALGORITHM = "HS256"
TOKEN_EXP = timedelta(days=7)
LLM_ENGINE_URL = "http://127.1.1.0:8081/llm-engine"
DATABASE_URL: str = "postgresql://postgres:root@localhost:5432/celestixai-backend"
FILE_STORAGE_PATH: str = os.path.join(os.getcwd(), "dataset_storage")
if not os.path.exists(FILE_STORAGE_PATH):
    os.mkdir(FILE_STORAGE_PATH)
# DATABASE_URL: str = "postgresql://user:password@localhost/dbname"
