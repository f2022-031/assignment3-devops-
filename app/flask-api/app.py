import os
import time
from typing import Optional

import pymysql
from flask import Flask, jsonify

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "mysql")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "flaskuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "flaskpass")
DB_NAME = os.getenv("DB_NAME", "flaskdb")


def get_connection() -> Optional[pymysql.connections.Connection]:
    """Connect to MySQL with a short retry loop for startup race conditions."""
    retries = 15
    delay_seconds = 2

    for _ in range(retries):
        try:
            return pymysql.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True,
            )
        except pymysql.MySQLError:
            time.sleep(delay_seconds)
    return None


def ensure_table() -> bool:
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS health_checks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            cursor.execute("INSERT INTO health_checks () VALUES ();")
        return True
    except pymysql.MySQLError:
        return False
    finally:
        conn.close()


@app.get("/")
def home():
    return jsonify(
        {
            "message": "Flask API is running",
            "service": "flask-api",
        }
    )


@app.get("/health")
def health():
    db_ready = ensure_table()
    status_code = 200 if db_ready else 503
    return (
        jsonify(
            {
                "api": "ok",
                "database": "ok" if db_ready else "unavailable",
            }
        ),
        status_code,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
