from database.db import get_connection

try:
    connection = get_connection()

    if connection.is_connected():
        print("✅ Database Connected Successfully!")

    connection.close()

except Exception as e:
    print("❌ Connection Failed!")
    print(e)