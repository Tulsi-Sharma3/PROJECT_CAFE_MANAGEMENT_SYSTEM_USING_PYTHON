from werkzeug.security import generate_password_hash
from database.db import get_connection

connection = get_connection()
cursor = connection.cursor()

username = "admin"
password = generate_password_hash("admin123")

query = """
INSERT INTO users (username, password)
VALUES (%s, %s)
"""

cursor.execute(query, (username, password))
connection.commit()

print("✅ Admin user created successfully!")

cursor.close()
connection.close()