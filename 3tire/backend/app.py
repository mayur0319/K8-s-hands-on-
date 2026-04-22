import os
import time

import mysql.connector
from flask import Flask, jsonify, request

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db-service")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppass")
DB_NAME = os.getenv("DB_NAME", "coderdb")

# Retry logic on startup
def wait_for_database(max_retries=30, delay=2):
    """Wait for database to be ready before starting the app."""
    for attempt in range(max_retries):
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                auth_plugin="mysql_native_password",
                connection_timeout=5,
            )
            cursor = conn.cursor(buffered=True)
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            conn.close()
            print(f"✓ Database connected on attempt {attempt + 1}")
            return True
        except Exception as e:
            print(f"✗ Database connection failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
    return False


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        auth_plugin="mysql_native_password",
        connection_timeout=5,
    )


def fetch_messages(limit=20):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, text FROM messages ORDER BY id DESC LIMIT %s",
        (limit,),
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


@app.route("/api/message")
def message():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT text FROM messages ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return jsonify({"message": row[0]})
        return jsonify({"message": "No message found in database"}), 404
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/api/messages", methods=["GET"])
def list_messages():
    try:
        return jsonify({"messages": fetch_messages()})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/api/messages", methods=["POST"])
def create_message():
    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()

    if not text:
        return jsonify({"error": "text is required"}), 400

    if len(text) > 255:
        return jsonify({"error": "text must be 255 characters or fewer"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (text) VALUES (%s)", (text,))
        conn.commit()
        message_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"id": message_id, "text": text}), 201
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/health")
def health():
    try:
        conn = get_connection()
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({"status": "ok", "database": "connected"})
    except Exception as exc:
        return jsonify({"status": "unhealthy", "database": "disconnected", "error": str(exc)}), 503


if __name__ == "__main__":
    print("Waiting for database to be ready...")
    if wait_for_database():
        print("Starting Flask app...")
        app.run(host="0.0.0.0", port=5000)
    else:
        print("ERROR: Failed to connect to database after retries. Exiting.")
        exit(1)
