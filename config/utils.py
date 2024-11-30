import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
RELOAD = os.getenv("RELOAD")
if RELOAD.upper() == "TRUE":
    RELOAD = True
else:
    RELOAD = False
WORKERS = os.getenv("WORKERS")

AUTH_JWT_KEY = os.getenv("AUTH_JWT_KEY")

DB_URL = os.getenv("DB_URL")
DB_SCHEMA = os.getenv("DB_SCHEMA")

DROPBOX_APP_KEY = os.getenv("DROPBOX_APP_KEY")
DROPBOX_APP_SECRET = os.getenv("DROPBOX_APP_SECRET")
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")
DROPBOX_REFRESH_TOKEN = os.getenv("DROPBOX_REFRESH_TOKEN")

AZURE_ACCOUNT_NAME = os.getenv("AZURE_ACCOUNT_NAME")
AZURE_ACCOUNT_KEY = os.getenv("AZURE_ACCOUNT_KEY")
AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")