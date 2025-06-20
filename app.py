from flask import Flask, request
import datetime
import sqlite3
import os

app = Flask(__name__)

# Optional homepage route so root URL doesn't show 404
@app.route('/')
def home():
    return '✅ Vibration API is live!'

# Main POST endpoint for ESP8266 or any IoT device
@app.route('/vibration', methods=['POST'])
def log_vibration():
    data = request.json
    timestamp = datetime.datetime.now()

    # Save vibration event to local SQLite DB
    conn = sqlite3.connect('vibration.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS logs (timestamp TEXT, value TEXT)")
    c.execute("INSERT INTO logs (timestamp, value) VALUES (?, ?)", (str(timestamp), data.get('value', 'vibration')))
    conn.commit()
    conn.close()

    return {'status': 'logged'}, 200

# Required for Render — use dynamic port
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
