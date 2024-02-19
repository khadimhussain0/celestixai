import os
from datetime import timedelta

SECRET_KEY = "supersecritkey"
ALGORITHM = "HS256"
TOKEN_EXP = timedelta(days=7)
LLM_ENGINE_URL = "http://34.32.173.165:11435"
DATABASE_URL: str = "postgresql://postgres:root@localhost:5432/celestixai-backend"
FILE_STORAGE_PATH: str = os.path.join(os.getcwd(), "dataset_storage")
VECTOR_FILE_STORAGE_PATH: str = os.path.join(os.getcwd(), "vectorestore")
if not os.path.exists(FILE_STORAGE_PATH):
    os.mkdir(FILE_STORAGE_PATH)
if not os.path.exists(VECTOR_FILE_STORAGE_PATH):
    os.mkdir(VECTOR_FILE_STORAGE_PATH)
# DATABASE_URL: str = "postgresql://user:password@localhost/dbname"
