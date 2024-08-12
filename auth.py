from flask import Blueprint, render_template, request, redirect, url_for, session
import json
import os

auth_bp = Blueprint('auth', __name__)

# Path to the JSON file where user data will be stored
USER_FILE = 'users.json'

def load_users():
    """Load user data from the JSON file."""
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_users(users):
    """Save user data to the JSON file."""
    with open(USER_FILE, 'w') as file:
        json.dump(users, file, indent=4)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users:
            return "Username already exists. Please choose a different one."
        users[username] = password
        save_users(users)
        session['username'] = username
        return redirect(url_for('index'))
    return render_template('register.html')
