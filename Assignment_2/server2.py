from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create_user():
    user_id = request.form['id']
    name = request.form['name']
    email = request.form['email']

    response = subprocess.run([
        'curl', '-X', 'POST', 'http://localhost:5000/users',
        '-H', 'Content-Type: application/json',
        '-d', f'{{"id":"{user_id}", "name":"{name}", "email":"{email}"}}'
    ], capture_output=True, text=True)

    return response.stdout

if __name__ == '__main__':
    app.run(port=5001)
