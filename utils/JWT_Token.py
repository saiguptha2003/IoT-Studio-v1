import jwt
from datetime import datetime, timedelta
from flask import request, jsonify
from functools import wraps
from pytz import timezone
import os
SECRET_KEY =os.getenv('JWTTOKEN_KEY')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
def create_token(username,additional_claims=None,sessionRequired=180):
    payload = {
        "username": username,
        "exp": datetime.now(timezone("Asia/Kolkata")) + timedelta(minutes=sessionRequired) 
    }
    if additional_claims:
        payload.update(additional_claims)
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token

def decode_token(token):
    """Decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload  
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}

def token_required(f):
    """Decorator to protect routes that require authentication."""
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing"}), 401

        token = token.split(" ")[1] if " " in token else token
        decoded = decode_token(token)
        if "error" in decoded:
            return jsonify({"message": decoded["error"]}), 401

        kwargs["userid"] = decoded.get("user_id")
        kwargs["email"] = decoded.get("email")
        kwargs['username'] = decoded.get("username")
        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper