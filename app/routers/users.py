from fastapi import APIRouter, Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.users import UserRequest
from app.domain.users import User as UserDomain
from app.models.users import Token
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    domain = UserDomain(db)
    access_token = domain.login(form_data)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register")
async def register(user_request: UserRequest, db: Session = Depends(get_db)):
    domain = UserDomain(db)
    return domain.register(user_request)