from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from passlib.context import CryptContext
from session import get_db
from sqlalchemy.orm import Session
from ..schemas.user_schema import CreateUser, ChangePassword
from models.users import User 
from dependencies import (
    get_current_user, 
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
internal_server_exception = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="An unexpected error occurred"
)


@router.post('/create-user')
def create_user(req: CreateUser, db: db_dependency):
    try:
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
    
    except HTTPException as err:
        db.rollback()
        print("Error in add user: {}".format(err))
        raise internal_server_exception


@router.post('/token')
def generate_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    try:
        user = authenticate_user(form_data.username, form_data.password, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        token = generate_access_token(user.email, user.id, timedelta(minutes=20))
        return {"access_token": token, "token_type": "bearer"}
    
    except Exception as err:
        print("Error in generating token: {}".format(err))
        raise internal_server_exception


# requires authentication
@router.put('/change-password')
def change_password(req: ChangePassword, db: db_dependency, user: user_dependency):
    try:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not authenticated"
            )
        
        user_model = db.query(User).filter(User.id == user.get('user_id')).first()
        if not bcrypt_context.verify(req.old_password, user_model.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Perhaps old password is incorrect"
            )
        
        user_model.hashed_password = req.new_password
        # db.add(user_model)
        db.commit()
        db.refresh(user_model)
        
        return {
            'status': status.HTTP_200_OK,
            'message': "Password has been changed successfully."
        }
    
    except HTTPException as err:
        raise err
    
    except Exception as err:
        db.rollback()
        print("Error in changing the password: {}".format(err))
        raise internal_server_exception
    
