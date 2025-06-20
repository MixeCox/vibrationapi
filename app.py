from flask import Flask, request
import datetime
import sqlite3

app = Flask(__name__)

@app.route('/vibration', methods=['POST'])
def log_vibration():
    data = request.json
    timestamp = datetime.datetime.now()
    conn = sqlite3.connect('vibration.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS logs (timestamp TEXT, value TEXT)")
    c.execute("INSERT INTO logs (timestamp, value) VALUES (?, ?)", (str(timestamp), data.get('value', 'vibration')))
    conn.commit()
    conn.close()
    return {'status': 'logged'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
