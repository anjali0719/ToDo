from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import or_
from session import get_db
from models.todo import ToDo
from dependencies import get_current_user
from ..schemas.todo_schema import CreateOrUpdateTodo


router = APIRouter(
    prefix='/api/vi'
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post('/create-todo')
def create_todo(req: CreateOrUpdateTodo, user: user_dependency, db: db_dependency):
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

# list all the todo's for logged in user
@router.get('/get-todo')
def get_todo_list(user: user_dependency, db: db_dependency, search: str = None):
    todo_list = db.query(ToDo).filter(ToDo.user_id == user.get('user_id')).all()
    return todo_list

# search for specific todo with either title or description
@router.get('/todo')
def search_todo(user: user_dependency, db: db_dependency, search: str | None = None):
    query = db.query(ToDo).filter(ToDo.user_id == user.get('user_id'))
    if search:
        search = f"%{search}%"
        query = query.filter(
            or_(
                ToDo.title.ilike(search),
                ToDo.description.ilike(search)
            )
        )
  
    todo_list = query.all()
    return todo_list

# get todo based on id
@router.get('/todo/{todo_id}')
def get_todo(user: user_dependency, db: db_dependency, todo_id: int):
    todo = db.query(ToDo).filter(
        ToDo.user_id == user.get('user_id'),
        ToDo.id == todo_id
    ).first()

    return todo

# update todo desc || # mark as complete
@router.put('/update-todo/{todo_id}')
def update_todo(db: db_dependency, user: user_dependency, todo_id: int, req: CreateOrUpdateTodo):
    todo = db.query(ToDo).filter(
        ToDo.user_id == user.get('user_id'),
        ToDo.id == todo_id
    ).first()

    todo.title = req.title
    todo.description = req.description
    todo.add_to_favourites = req.add_to_favourites
    todo.completed = req.completed

    db.commit()
    db.refresh(todo)
    return todo


# delete todo
@router.delete('/delete-todo')
def delete_todo(db: db_dependency, user: user_dependency, todo_id: int):
    db.query(ToDo).filter(
        ToDo.user_id == user.get('user_id'),
        ToDo.id == todo_id
    ).delete()

    db.commit()
    return "Item has been deleted"
