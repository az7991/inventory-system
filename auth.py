import bcrypt
import sqlite3
import jwt
import datetime
import json
from db import connect_db
from cryptography.fernet import Fernet
import os

SECRET_KEY = "mysecretkey"
KEY_FILE = "secret.key"
PASSWORD_FILE = "passwords.enc"

def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)

def load_key():
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

generate_key()
fernet = Fernet(load_key())

import bcrypt

def hash_password(password: str) -> bytes:
    """Hashar ett lösenord."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


def encrypt_password(password):
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return fernet.decrypt(encrypted_password.encode()).decode()

def store_encrypted_passwords(passwords):
    with open(PASSWORD_FILE, "w") as file:
        json.dump(passwords, file)

def load_encrypted_passwords():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as file:
            return json.load(file)
    return {}

def create_user(username, password, role="staff"):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                    (username, hashed_password, role))
        conn.commit()
        print(f"Användare {username} skapades med roll '{role}'.")

        passwords = load_encrypted_passwords()
        passwords[username] = encrypt_password(password)
        store_encrypted_passwords(passwords)
    except sqlite3.IntegrityError:
        print("Användarnamnet är redan upptaget.")
    finally:
        conn.close()

def login(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
        stored_data = cursor.fetchone()

        if stored_data:
            stored_password, role = stored_data 
            
            if bcrypt.checkpw(password.encode(), stored_password):
                print(f"Användare {username} är inloggad.")
                
                token = create_jwt(username, role)
                return token
            else:
                print("Fel lösenord.")
                return None
        else:
            print("Användarnamn finns inte.")
            return None
    finally:
        conn.close()

def delete_user(username):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Användare {username} har tagits bort.")
        else:
            print(f"Inget användarnamn som heter {username} hittades.")
    except Exception as e:
        print(f"Ett fel uppstod: {e}")
    finally:
        conn.close()

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def create_jwt(username, role):
    payload = {
        'username': username,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expiration time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def decode_jwt(token):
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded_data
    except jwt.ExpiredSignatureError:
        print("Tokenen har gått ut.")
    except jwt.InvalidTokenError:
        print("Ogiltig token.")
    return None

def get_all_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users")
    users = cursor.fetchall()
    conn.close()
    return users








