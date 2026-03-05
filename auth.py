from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from datetime import datetime, timedelta, timezone
from database import get_db
from models import User
from schemas import TokenData
import os

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Support both bcrypt and pbkdf2_sha256 for backward compatibility
pwd_context = CryptContext(schemes=["bcrypt", "pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    """Verify a password against a hash, handling errors gracefully"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        # Hash format is not recognized - likely corrupted or wrong format
        return False
    except Exception as e:
        # Any other verification error
        print(f"⚠️ Password verification error: {e}")
        return False

def get_password_hash(password):
    """Hash a password using bcrypt"""
    return pwd_context.hash(password[:72])

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db: Session, email: str, password: str):
    """Authenticate a user by email and password"""
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            # User not found
            return None

        # Verify password
        if not verify_password(password, user.password_hash):
            # Password incorrect
            return None

        return user
    except Exception as e:
        print(f"⚠️ Authentication error: {e}")
        return None

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user
