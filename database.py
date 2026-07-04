import sqlite3
import json
from datetime import datetime

DB_PATH = 'parking_history.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            filename TEXT,
            vehicle_count INTEGER,
            vehicles_json TEXT,
            image_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_request(filename, vehicle_count, vehicles_list, image_path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO requests (timestamp, filename, vehicle_count, vehicles_json, image_path)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        datetime.now().isoformat(),
        filename,
        vehicle_count,
        json.dumps(vehicles_list),
        image_path
    ))
    conn.commit()
    conn.close()

def get_history(limit=50):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT timestamp, filename, vehicle_count, vehicles_json, image_path
        FROM requests ORDER BY id DESC LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows