from flask import Flask, request, jsonify, send_from_directory
import psycopg
import uuid
from dotenv import load_dotenv
import os
from flask_cors import CORS, cross_origin

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory('../fronend', 'index.html')

# NeonDB connection
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    return psycopg.connect(DATABASE_URL)

# Create table if not exists
with get_db_connection() as conn:
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                message_id UUID PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL
            )
        """)

@cross_origin()
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    message_id = str(uuid.uuid4())

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO messages (message_id, name, email, message)
                    VALUES (%s, %s, %s, %s)
                """, (message_id, name, email, message))
        return jsonify({"status": "success", "message_id": message_id})
    except Exception as e:
        app.logger.error('DB insert failed: %s', e)
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)