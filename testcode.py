import os
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# --- VULNERABILITY 1: SQL Injection ---
@app.route("/login")
def login():
    username = request.args.get("user")
    password = request.args.get("pass")
    
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # 🔥 Vulnerable to SQL Injection
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    
    if cursor.fetchone():
        return "Login successful!"
    else:
        return "Invalid credentials."

# --- VULNERABILITY 2: OS Command Injection ---
@app.route("/ping")
def ping():
    ip = request.args.get("ip")
    
    # 🔥 Vulnerable to OS Command Injection
    response = os.popen(f"ping -c 1 {ip}").read()
    return f"<pre>{response}</pre>"

if __name__ == "__main__":
    app.run(debug=True)
