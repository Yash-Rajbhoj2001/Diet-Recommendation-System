import streamlit as st
import jwt
from .database import check_and_initialize_db
check_and_initialize_db()  # This ensures DB and users table are ready
from .database import get_user_by_email, add_user
from .security import verify_password, hash_password

# Set up JWT secrets (ensure these are set appropriately somewhere in your app)
JWT_SECRET = "your_jwt_secret_key"
JWT_ALGORITHM = "HS256"

import datetime

def create_jwt_token(payload: dict, expires_in_minutes=60):
    """Generate JWT token with expiration"""
    payload = payload.copy()
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_in_minutes)
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def is_authenticated():
    """Check if user is authenticated"""
    token = st.session_state.get("auth_token")
    if token:
        try:
            jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
    return False

def get_current_user():
    """Get current user's email from JWT"""
    token = st.session_state.get("auth_token")
    if token:
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return payload.get("email")
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    return None

def authenticate_user(email: str, password: str):
    """Authenticate user credentials"""
    user = get_user_by_email(email)
    if not user:
        return False, "User not found"
    
    if verify_password(user[2], password):
        jwt_token = create_jwt_token({"email": email})
        st.session_state["auth_token"] = jwt_token
        return True, "Authentication successful"
    return False, "Invalid credentials"

def register_user(email: str, password: str):
    """Register a new user"""
    if get_user_by_email(email):
        return False, "Email already registered"
    
    password_hash = hash_password(password)
    try:
        add_user(email, password_hash)
        return True, "Registration successful"
    except Exception as e:
        return False, f"Registration failed: {str(e)}"

def logout():
    """Clear authentication session"""
    if "auth_token" in st.session_state:
        del st.session_state["auth_token"]
    st.session_state.clear()
