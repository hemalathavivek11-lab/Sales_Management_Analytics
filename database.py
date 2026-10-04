import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "sales_management"),
    "autocommit": True,
    "charset": "utf8mb4",
    "raise_on_warnings": True,
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def create_database():
    setup_config = DB_CONFIG.copy()
    setup_config.pop("database", None)

    connection = mysql.connector.connect(**setup_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        print(f"Database '{DB_CONFIG['database']}' created or already exists.")
    finally:
        connection.close()

    connection = get_connection()
    try:
        schema_path = Path(__file__).with_name("schema.sql")
        schema_sql = schema_path.read_text(encoding="utf-8")
        statements = []
        for statement in schema_sql.split(";"):
            cleaned = statement.strip()
            if cleaned:
                if cleaned.upper().startswith("CREATE DATABASE"):
                    continue
                if cleaned.upper().startswith("USE "):
                    continue
                statements.append(cleaned)

        with connection.cursor() as cursor:
            for statement in statements:
                cursor.execute(statement)
        print("Schema applied successfully.")
    finally:
        connection.close()


if __name__ == "__main__":
    create_database()