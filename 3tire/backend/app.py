import os
import mysql.connector
from flask import Flask, jsonify

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db-service")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppass")
DB_NAME = os.getenv("DB_NAME", "coderdb")


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        auth_plugin="mysql_native_password",
        connection_timeout=5,
    )


@app.route("/api/message")
def message():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT text FROM messages ORDER BY id LIMIT 1")
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return jsonify({"message": row[0]})
        return jsonify({"message": "No message found in database"}), 404
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
