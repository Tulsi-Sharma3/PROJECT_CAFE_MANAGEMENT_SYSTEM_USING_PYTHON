import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

DB_PORT = int(os.getenv("DB_PORT", "4000"))
DB_SSL_CA = os.getenv("DB_SSL_CA")

SECRET_KEY = os.getenv("SECRET_KEY")