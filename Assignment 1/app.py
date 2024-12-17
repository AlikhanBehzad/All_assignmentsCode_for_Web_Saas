from flask import Flask, request, jsonify, redirect, url_for
import json
import os

app = Flask(__name__)
print("Hello World")
# Path to the text file used as a simple database for storing user data
USER_DATA_FILE = 'users_data.txt'


def load_users():
    """Load users data from the text file (in-memory)."""
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_users(users):
    """Save users data to the text file."""
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)


@app.route('/')
def index():
    return "Welcome to the Flask User Profile Management System!"


@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    email = data.get('email')
    age = data.get('age')

    if not email or not age:
        return jsonify({"error": "Email and Age are required!"}), 400

    users = load_users()

    if email in users:
        return jsonify({"error": "User with this email already exists!"}), 400

    users[email] = {'email': email, 'age': age}
    save_users(users)
    return jsonify({"message": "User registered successfully!"}), 201


@app.route('/get_user/<email>', methods=['GET'])
def get_user(email):
    users = load_users()
    
    if email not in users:
        return jsonify({"error": "User not found!"}), 404
    
    return jsonify(users[email])


@app.route('/update_user/<email>', methods=['PUT'])
def update_user(email):
    data = request.get_json()
    age = data.get('age')

    if not age:
        return jsonify({"error": "Age is required!"}), 400

    users = load_users()

    if email not in users:
        return jsonify({"error": "User not found!"}), 404

    users[email]['age'] = age
    save_users(users)
    return jsonify({"message": "User updated successfully!"})


@app.route('/delete_user/<email>', methods=['DELETE'])
def delete_user(email):
    users = load_users()

    if email not in users:
        return jsonify({"error": "User not found!"}), 404

    del users[email]
    save_users(users)
    return jsonify({"message": "User deleted successfully!"})


if __name__ == '__main__':
    app.run(debug=True)



