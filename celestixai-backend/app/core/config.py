import os
from datetime import timedelta

SECRET_KEY = "supersecritkey"
ALGORITHM = "HS256"
TOKEN_EXP = timedelta(days=7)
DATABASE_URL: str = "sqlite:///./test.db"
FILE_STORAGE_PATH: str = os.path.join(os.getcwd(), "dataset_storage")
if not os.path.exists(FILE_STORAGE_PATH):
    os.mkdir(FILE_STORAGE_PATH)
# DATABASE_URL: str = "postgresql://user:password@localhost/dbname"
