from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from passlib.context import CryptContext
from session import get_db
from sqlalchemy.orm import Session
from ..schemas.user_schema import CreateUserRequest, ChangePasswordRequest
from ..schemas.user_schema import CreateUserRequest
from ..services.user_services import (
    add_user, 
    get_current_user, 
    change_user_password, 
    authenticate_user, 
    generate_access_token
)

router = APIRouter(
    prefix='/api/vi'
)

db_dependency = Annotated[Session, Depends(get_db)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post('/create-user')
def create_user(req: CreateUserRequest, db: db_dependency):
    return add_user(req, db)

@router.post('/token')
def generate_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized"
        )
    
    token = generate_access_token(form_data.username, form_data.client_id, timedelta(minutes=20))
    return token

@router.put('/change-password')
def change_password(req: ChangePasswordRequest, db: db_dependency, user: user_dependency):
    return change_user_password(req, db, user)

