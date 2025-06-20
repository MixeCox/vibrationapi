from flask import Flask, request, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# Database setup
DB_NAME = "vibration.db"

def init_db():
    """Initialize the database with a logs table"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            value TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Initialize database when app starts
init_db()

@app.route('/')
def home():
    return '✅ Vibration API is live! Use POST /vibration to log data and GET /logs to view records'

@app.route('/vibration', methods=['POST'])
def log_vibration():
    # Check if request contains JSON
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    
    # Validate required field
    if 'value' not in data:
        return jsonify({"error": "Missing 'value' field"}), 400
    
    # Store in database
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(
            "INSERT INTO logs (timestamp, value) VALUES (?, ?)",  # FIXED: Added missing parenthesis
            (datetime.now().isoformat(), str(data['value']))
        )
        conn.commit()
        return jsonify({
            "status": "success",
            "message": "Vibration logged",
            "data": data
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/logs', methods=['GET'])
def get_logs():
    """Endpoint to view all logged vibrations"""
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM logs ORDER BY timestamp DESC")
        logs = [{
            "id": row[0],
            "timestamp": row[1],
            "value": row[2]
        } for row in c.fetchall()]
        return jsonify({"logs": logs})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)