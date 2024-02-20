import os
from datetime import timedelta

SECRET_KEY = "supersecritkey"
ALGORITHM = "HS256"
TOKEN_EXP = timedelta(days=7)
LLM_ENGINE_URL = "http://34.32.173.165:11435"
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "celestixai-backend")
DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
FILE_STORAGE_PATH: str = os.path.join(os.getcwd(), "dataset_storage")
VECTOR_FILE_STORAGE_PATH: str = os.path.join(os.getcwd(), "vectorestore")
if not os.path.exists(FILE_STORAGE_PATH):
    os.mkdir(FILE_STORAGE_PATH)
if not os.path.exists(VECTOR_FILE_STORAGE_PATH):
    os.mkdir(VECTOR_FILE_STORAGE_PATH)
# DATABASE_URL: str = "postgresql://user:password@localhost/dbname"
