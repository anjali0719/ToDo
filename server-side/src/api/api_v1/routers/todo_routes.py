import datetime
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from session import get_db
from models.todo import ToDo
from dependencies import get_current_user
from ..schemas.todo_schema import CreateOrUpdateTodo, ToDoListResponse


router = APIRouter(
    prefix='/api/vi'
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

today = datetime.date.today()
internal_server_exception = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="An unexpected error occurred"
)
todo_404 = HTTPException(
    status_code= status.HTTP_404_NOT_FOUND,
    detail="ToDo not found" 
)


@router.post('/create-todo')
def create_todo(req: CreateOrUpdateTodo, user: user_dependency, db: db_dependency):
    todo = ToDo(
        title= req.title,
        description= req.description,
        add_to_favourites= req.add_to_favourites,
        completed= req.completed,
        scheduled_for= req.scheduled_for,
        user_id= user.get('user_id')
    )

    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


# list all the todo's for logged in user
@router.get('/todo-list', response_model=ToDoListResponse)
def todo_list(
    user: user_dependency, 
    db: db_dependency,  
    params: Params = Depends(),
    search: str | None = None, 
    filter_type: str = "today",
):
    
    today = date.today()
    user_id = user.get('user_id')

    base_query = db.query(ToDo).filter(ToDo.user_id == user_id)
    
    counts_query = db.query(
        func.sum(case(
            (ToDo.scheduled_for == today, 1), else_=0)
        ).label("today_count"),
        func.sum(case(
            (ToDo.scheduled_for > today, 1), else_=0)
        ).label("upcoming_count"),
        func.sum(case(
            (ToDo.add_to_favourites.is_(True), 1), else_=0)
        ).label("fav_count"),
        func.sum(case(
            (ToDo.completed.is_(True), 1), else_=0)
        ).label("completed_count")
    ).filter(ToDo.user_id == user_id, ToDo.completed.is_(False))

    count_row = counts_query.first()

    counts = {
        "today": count_row.today_count or 0,
        "upcoming": count_row.upcoming_count or 0,
        "favourites": count_row.fav_count or 0,
        "completed": count_row.completed_count or 0
    }

    filter_conditions = {
        "today": [ToDo.scheduled_for == today, ToDo.completed.is_(False)],
        "upcoming": [ToDo.scheduled_for > today, ToDo.completed.is_(False)],
        "favourites": [ToDo.add_to_favourites.is_(True), ToDo.completed.is_(False)], 
        "completed": [ToDo.completed.is_(True)],
    }
    
    conditions = filter_conditions.get(filter_type, filter_conditions["today"])
    todo_list = base_query.filter(*conditions)

    if search:
        search = f"%{search}%"
        todo_list = todo_list.filter(ToDo.title.ilike(search))
        
    paginated_result = paginate(todo_list, params)
    return {
        "counts": counts,
        "results": paginated_result
    }



# search for specific todo with either title or description
# @router.get('/todo')
# def search_todo(user: user_dependency, db: db_dependency, search: str | None = None):
#     query = db.query(ToDo).filter(ToDo.user_id == user.get('user_id'))
#     if search:
#         search = f"%{search}%"
#         query = query.filter(
#             or_(
#                 ToDo.title.ilike(search),
#                 ToDo.description.ilike(search)
#             )
#         )
  
#     todo_list = query.all()
#     return todo_list


# get todo based on id
# @router.get('/todo/{todo_id}')
# def get_todo(user: user_dependency, db: db_dependency, todo_id: int):
#     try:
#         todo = db.query(ToDo).filter(
#             ToDo.user_id == user.get('user_id'),
#             ToDo.id == todo_id
#         ).first()

#         if not todo:
#             raise todo_404
        
#         return todo

#     except HTTPException as err:
#         raise err
    
#     except Exception as err:
#         db.rollback()
#         print("Error in fetching the todo: {}".format(err))
#         raise internal_server_exception


# update todo desc || # mark as complete
@router.put('/update-todo/{todo_id}')
def update_todo(db: db_dependency, user: user_dependency, todo_id: int, req: CreateOrUpdateTodo):
    try:
        todo = db.query(ToDo).filter(
            ToDo.user_id == user.get('user_id'),
            ToDo.id == todo_id
        ).first()

        if not todo:
            raise todo_404
        
        todo.title = req.title
        todo.description = req.description
        todo.add_to_favourites = req.add_to_favourites
        todo.completed = req.completed
        todo.scheduled_for = req.scheduled_for

        db.commit()
        db.refresh(todo)
        return todo
    
    except HTTPException as err:
        raise err
    
    except Exception as err:
        db.rollback()
        print("Error in update: {}".format(err))
        raise internal_server_exception


# delete todo
@router.delete('/delete-todo')
def delete_todo(db: db_dependency, user: user_dependency, todo_id: int):
    try:
        todo = db.query(ToDo).filter(
            ToDo.user_id == user.get('user_id'),
            ToDo.id == todo_id
        ).delete()

        if not todo:
            raise todo_404
        
        db.commit()
        return {
            'status': status.HTTP_200_OK,
            'message': "ToDo item has been deleted"
        }
    except HTTPException as err:
        raise err
    
    except Exception as err:
        db.rollback()
        print("Error in delete: {}".format(err))
        raise internal_server_exception

