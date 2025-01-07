import secrets
from fastapi import HTTPException
from jose import jwt
from datetime import timedelta, timezone, datetime

# Generate a secret key (to be stored securely in production)
secret = secrets.token_hex(32)
algorithm = "HS256"
access_token_days = 45  # Expiration in days

def create_access_token(data: dict):
    encode = data.copy()
    # Update expiration to use days, not minutes
    expire = datetime.now(timezone.utc) + timedelta(days=access_token_days)
    encode.update({"exp": expire})
    encode.update({"id": data["id"]})
    my_jwt = jwt.encode(encode, secret, algorithm=algorithm)
    return my_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, secret, algorithms=[algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token Expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
