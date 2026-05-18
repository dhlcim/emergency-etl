import pymysql
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def get_cloud_connection():
    return pymysql.connect(
        host=os.getenv("CLOUD_DB_HOST"),
        port=int(os.getenv("CLOUD_DB_PORT")),
        user=os.getenv("CLOUD_DB_USER"),
        password=os.getenv("CLOUD_DB_PASSWORD"),
        db=os.getenv("CLOUD_DB_NAME"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )