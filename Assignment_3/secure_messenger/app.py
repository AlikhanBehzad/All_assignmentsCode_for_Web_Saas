from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import os
import cryptography 
# Initialize Flask app
app = Flask(__name__)

# Generate encryption key if not present
KEY_FILE = "secret.key"
if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
else:
    with open(KEY_FILE, "rb") as key_file:
        key = key_file.read()

fernet = Fernet(key)

# In-memory message storage
messages = {}

@app.route("/send_message", methods=["POST"])
def send_message():
    try:
        data = request.json
        user = data.get("user")
        message = data.get("message")

        if not user or not message:
            return jsonify({"error": "Both 'user' and 'message' are required."}), 400

        # Encrypt and store message
        encrypted_message = fernet.encrypt(message.encode()).decode()
        messages[user] = encrypted_message

        return jsonify({"status": "Message stored securely!"}), 201
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@app.route("/get_message", methods=["GET"])
def get_message():
    try:
        user = request.args.get("user")
        if not user or user not in messages:
            return jsonify({"error": "User not found."}), 404

        encrypted_message = messages[user]
        decrypted_message = fernet.decrypt(encrypted_message.encode()).decode()

        return jsonify({"message": decrypted_message}), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
