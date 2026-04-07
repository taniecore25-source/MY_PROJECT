from flask import Flask, request, jsonify, send_from_directory
import json
import uuid
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(__file__)
FRONTEND_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', 'fronend'))
MESSAGES_FILE = os.path.join(BASE_DIR, 'messages.json')

@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(FRONTEND_DIR, path)


def ensure_messages_file():
    if not os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=2)


def read_messages():
    ensure_messages_file()
    with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_messages(messages):
    with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, indent=2)

ensure_messages_file()


@cross_origin()
@app.route('/send_message', methods=['POST'])
def send_message():
    print("=== DEBUG: Received message submission ===")
    data = request.get_json(silent=True)
    print(f"DEBUG: Received data: {data}")
    
    if not data:
        print("DEBUG: Invalid JSON payload")
        return jsonify({"status": "error", "error": "Invalid JSON payload"}), 400

    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip()
    message = (data.get('message') or '').strip()
    
    print(f"DEBUG: Parsed data - Name: {name}, Email: {email}, Message: {message}")

    if not name or not email or not message:
        print("DEBUG: Missing required fields")
        return jsonify({"status": "error", "error": "Name, email, and message are required"}), 400

    message_id = str(uuid.uuid4())
    entry = {
        "message_id": message_id,
        "name": name,
        "email": email,
        "message": message
    }
    
    print(f"DEBUG: Created entry: {entry}")

    try:
        messages = read_messages()
        print(f"DEBUG: Read existing messages: {messages}")
        messages.append(entry)
        write_messages(messages)
        print(f"DEBUG: Successfully saved message with ID: {message_id}")
        return jsonify({"status": "success", "message_id": message_id})
    except Exception as e:
        print(f"DEBUG: Error saving message: {e}")
        app.logger.error('Failed to save message: %s', e)
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)