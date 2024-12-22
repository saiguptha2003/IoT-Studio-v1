import jwt
from datetime import datetime, timedelta
from flask import request, jsonify
from functools import wraps

SECRET_KEY = """Re6mYT/HN7aelApSsrQV7vzooBKNLjZCHGkMZLHJN2N0I8ErWnlLAVatKhy+flgS
iwIXuu1pqLI5aRus77YBdJw//c7Bsq5JGXtSzTfLNSNJ6gS2jhJ+7HBeCAaqNWFO
5HY0wCuYgJ1LtBUHSS69Ywoyx+gPlAJ8Ej29nnb7th0Za4hHTtzWZslWcBWT384P
t492g1Xp2zgDM0WOuv3oSRrsdo7p+twJATLeTGfrhXqvN4GX3BJ88WGky2L+n67C
R0+PcVBmz34C3SKxv+Y3/qejkZoQXkHj7U0owh2678vTVDzFev6BtvmZ/g8LiwWP
zs7dxYwcHi9RHfZA6QtczA=="""
def create_token(username,additional_claims=None):
    payload = {
        "username": username,
        "exp": datetime.utcnow() + timedelta(hours=2)  
    }
    if additional_claims:
        payload.update(additional_claims)
    
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def decode_token(token):
    """Decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
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