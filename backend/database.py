import sqlite3
from datetime import datetime

DB_NAME = "documents.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            filetype TEXT,
            chunks INTEGER,
            upload_time TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_document(filename, filetype, chunks):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO documents (filename, filetype, chunks, upload_time)
        VALUES (?, ?, ?, ?)
    """, (
        filename,
        filetype,
        chunks,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_all_documents():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM documents")
    rows = cursor.fetchall()

    conn.close()
    return rows