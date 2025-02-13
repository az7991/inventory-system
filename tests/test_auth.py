import pytest
import bcrypt  # Lägg till detta import
from auth import hash_password, create_jwt, decode_jwt

def test_hash_password():
    password = "supersecurepassword"
    hashed = hash_password(password)
    assert hashed != password  # Se till att lösenordet är hashat och inte lika med originalet
    assert bcrypt.checkpw(password.encode(), hashed)  # Verifiera att hashningen fungerar

def test_jwt():
    token = create_jwt("testuser", "admin")
    decoded = decode_jwt(token)
    assert decoded['username'] == "testuser"  # Verifiera att användarnamnet är korrekt
    assert decoded['role'] == "admin"  # Verifiera att rollen är korrekt
    assert 'exp' in decoded  # Verifiera att utgångsdatumet finns



