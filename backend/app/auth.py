from jose import jwt, JWTError
from fastapi import HTTPException, Header
from datetime import datetime, timedelta
import logging

SECRET_KEY = "replace-this-before-submission"
ALGORITHM = "HS256"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("healthcare-auth")

users = {
    "patient": {
        "id": "u1",
        "username": "patient",
        "password": "patient123",
        "role": "patient",
    },
    "doctor": {
        "id": "u2",
        "username": "doctor",
        "password": "doctor123",
        "role": "doctor",
    },
}

def login_user(username: str, password: str):
    user = users.get(username)
    if not user or password != user["password"]:
        logger.error("Invalid credentials")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    logger.info("Login success for user %s", username)

    payload = {
        "sub": user["id"],
        "username": user["username"],
        "role": user["role"],
        "exp": datetime.utcnow() + timedelta(hours=4),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer", "role": user["role"]}

def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.replace("Bearer ", "")
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        logger.error("Invalid token")
        raise HTTPException(status_code=401, detail="Invalid token")