from fastapi import APIRouter, Depends
from ..schemas.todo_schema import CreateTodo
from dependencies import get_current_user
from typing import Annotated
from session import get_db
from sqlalchemy.orm import Session
from models.todo import ToDo


router = APIRouter(
    prefix='/api/vi'
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post('/create-todo')
def create_todo(req: CreateTodo, user: user_dependency, db: db_dependency):
    todo = ToDo(
        title= req.title,
        description= req.description,
        add_to_favourites= req.add_to_favourites,
        completed= req.completed,
        user_id= user.get('user_id')
    )

    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo
