from fastapi import HTTPException, status
from app.crud.users import User as UserCrud
from passlib.context import CryptContext
import os
from datetime import datetime, timedelta, timezone
import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))

class User:
    def __init__(self, db):
        self.crud = UserCrud(db)

    def hash_password(self, password):
        return pwd_context.hash(password)
    
    def create_access_token(self, data, expires_delta):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def register(self, user_request):
        user = self.crud.get_user(user_request.username)
        if user:
            return HTTPException(status_code=400, detail="Username already exists")
        
        hashed_password = self.hash_password(user_request.password)
        self.crud.register(user_request, hashed_password)
        return HTTPException(status_code=200, detail="Registration went successfully")
    

    def login(self, form_data):
        user = self.crud.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return access_token