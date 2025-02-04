from fastapi import FastAPI
from fastapi_pagination import add_pagination
from session import Base, engine
from api.api_v1.routers import user_routes, todo_routes

app = FastAPI()
Base.metadata.create_all(engine)

app.include_router(user_routes.router)
app.include_router(todo_routes.router)

add_pagination(app)
# TO BE IMPLEMENETED:
'''
1. forgot password
2. pagination
3. Order the todo's in order by scheduled_for > updated_at
4. Create a back ref in ToDo model for User model so that all the dets can be accessed easily

We can try this(using celery):
Mark a todo for some scheduled date, send the user a reminder and then once date has been passed mark the status as incomplete or complete
'''
