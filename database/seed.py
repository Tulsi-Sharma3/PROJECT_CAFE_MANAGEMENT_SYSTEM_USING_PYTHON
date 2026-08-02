from database.db import get_connection
from werkzeug.security import generate_password_hash


conn = get_connection()
cursor = conn.cursor()


password = generate_password_hash("admin123")


query = """
INSERT INTO users(username,password,role)
VALUES(%s,%s,%s)
"""


cursor.execute(
    query,
    ("admin",password,"admin")
)


conn.commit()

print("Admin Created")

conn.close()