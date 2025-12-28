"""
Authentication handlers for the WebRTC communication app.
"""
import os
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import jwt, JWTError
import bcrypt


# Configuration
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", secrets.token_hex(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24


# In-memory user storage (replace with database in production)
users_db: Dict[str, dict] = {}


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode(), hashed.encode())


def create_access_token(user_id: str, username: str) -> str:
    """Create a JWT access token."""
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode = {
        "sub": user_id,
        "username": username,
        "exp": expire,
        "iat": datetime.utcnow()
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> Optional[dict]:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def generate_user_id() -> str:
    """Generate a unique user ID."""
    return secrets.token_hex(16)


async def register_user(username: str, password: str) -> dict:
    """Register a new user."""
    # Check if username exists
    for user in users_db.values():
        if user["username"].lower() == username.lower():
            return {"success": False, "error": "Username already exists"}
    
    # Validate input
    if len(username) < 3:
        return {"success": False, "error": "Username must be at least 3 characters"}
    if len(password) < 6:
        return {"success": False, "error": "Password must be at least 6 characters"}
    
    # Create user
    user_id = generate_user_id()
    users_db[user_id] = {
        "user_id": user_id,
        "username": username,
        "password_hash": hash_password(password),
        "created_at": datetime.utcnow().isoformat()
    }
    
    # Generate token
    token = create_access_token(user_id, username)
    
    return {
        "success": True,
        "user_id": user_id,
        "username": username,
        "token": token
    }


async def login_user(username: str, password: str) -> dict:
    """Authenticate a user."""
    # Find user by username
    user = None
    for u in users_db.values():
        if u["username"].lower() == username.lower():
            user = u
            break
    
    if not user:
        return {"success": False, "error": "Invalid username or password"}
    
    # Verify password
    if not verify_password(password, user["password_hash"]):
        return {"success": False, "error": "Invalid username or password"}
    
    # Generate token
    token = create_access_token(user["user_id"], user["username"])
    
    return {
        "success": True,
        "user_id": user["user_id"],
        "username": user["username"],
        "token": token
    }


async def get_user_from_token(token: str) -> Optional[dict]:
    """Get user information from a token."""
    payload = verify_token(token)
    if not payload:
        return None
    
    user_id = payload.get("sub")
    if user_id and user_id in users_db:
        user = users_db[user_id]
        return {
            "user_id": user["user_id"],
            "username": user["username"]
        }
    return None
