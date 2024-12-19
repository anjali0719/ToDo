from fastapi import APIRouter, Depends
from typing import Annotated
from session import get_db
from sqlalchemy.orm import Session

from ..schemas.user_schema import CreateUserRequest
from ..services.user_services import add_user

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]


@router.post('/create-user')
def create_user(req: CreateUserRequest, db: db_dependency):
    return add_user(req, db)
