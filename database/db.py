import mysql.connector
from config.db_config import (
    DB_HOST, DB_USER, DB_PASSWORD, DB_NAME,
    DB_PORT, DB_SSL_CA
)


def get_connection():
    connection = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        ssl_ca=DB_SSL_CA,
        ssl_verify_cert=True
    )
    return connection