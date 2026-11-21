import os 
from dotenv import load_dotenv

load_dotenv()

class config:
    
    DB_HOST = os.get.env("DB_HOST", "localhost")
    DB_USER =  os.get.env("DB_USER")
    DB_PASSWORD =  os.get.env("DB_PASSWORD")
    DB_NAME =  os.get.env("DB_NAME")

    SECRET_KEY =  os.get.env("SECRET_KEY")
