from datetime import timedelta, datetime, timezone
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from models.users import User
from typing import Annotated
from fastapi import Depends, HTTPException, status
from ..schemas.user_schema import CreateUserRequest, ChangePasswordRequest
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from session import get_db

from dotenv import load_dotenv
import os
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

db_dependency = Annotated[Session, Depends(get_db)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")


# verifies if the email and password are correct!
def authenticate_user(email: str, password: str, db: db_dependency):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

# generates token
def generate_access_token(email: str, user_id: int, expires_in: timedelta):
    encode = { 'sub': email, 'id': user_id }
    expires = datetime.now(timezone.utc) + expires_in
    encode.update({ 'exp': expires })
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# gets you the logged-in user
def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get('sub')
        user_id = payload.get('id')
        if email is None and user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email and password not provided"
            )
        return { 'email': email, 'user_id': user_id }
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized"
        )


def add_user(req: CreateUserRequest, db: Session):
    user = User(
        first_name= req.first_name,
        last_name= req.last_name,
        hashed_password= bcrypt_context.hash(req.password),
        email= req.email,
        is_active= True
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'is_active': user.is_active
    }

# requires authentication
def change_user_password(req: ChangePasswordRequest, db: Session, user: Annotated[dict, Depends(get_current_user)]):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )
    
    user_model = db.query(User).filter(User.id == user.get('id')).first()
    if not bcrypt_context.verify(req.old_password, user_model.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Perhaps old password is incorrect"
        )
    
    user_model.hashed_password = req.new_password
    db.add(user_model)
    db.commit()
    db.refresh(user_model)


