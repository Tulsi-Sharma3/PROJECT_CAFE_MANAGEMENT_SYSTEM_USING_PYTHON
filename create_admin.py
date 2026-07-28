from werkzeug.security import generate_password_hash
from database.db import get_connection

connection = get_connection()
cursor = connection.cursor()

password = generate_password_hash("admin123")

cursor.execute(
    """
    INSERT INTO users(username,password)
    VALUES(%s,%s)
    """,
    ("admin", password)
)

connection.commit()

print("Admin Created Successfully!")

cursor.close()
connection.close()