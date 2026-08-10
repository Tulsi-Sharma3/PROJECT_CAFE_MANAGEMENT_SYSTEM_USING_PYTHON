import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from database.db import get_connection

load_dotenv()

username = "admin"
password = os.getenv("ADMIN_PASSWORD")

if not password:
    raise ValueError("ADMIN_PASSWORD is not set in .env")

connection = get_connection()
cursor = connection.cursor()

hashed_password = generate_password_hash(password)

query = """
INSERT INTO users (username, password)
VALUES (%s, %s)
"""

cursor.execute(query, (username, hashed_password))
connection.commit()

print("✅ Admin user created successfully!")

cursor.close()
connection.close()