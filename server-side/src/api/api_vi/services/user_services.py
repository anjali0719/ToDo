from sqlalchemy.orm import Session
from models.users import User
from ..schemas.user_schema import CreateUserRequest

def add_user(req: CreateUserRequest, db: Session):
    user = User(
        first_name= req.first_name,
        last_name= req.last_name,
        hashed_password= req.password,
        email= req.email,
        is_active= True
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

