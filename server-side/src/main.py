from fastapi import FastAPI
from session import Base, engine
from api.api_v1.routers import user_routes, todo_routes

app = FastAPI()
Base.metadata.create_all(engine)

app.include_router(user_routes.router)
app.include_router(todo_routes.router)


# TO BE IMPLEMENETED:
'''
1. forgot password
2. pagination
3. Order the todo's in order by scheduled_for > updated_at

We can try this(using celery):
Mark a todo for some scheduled date, send the user a reminder and then once date has been passed mark the status as incomplete or complete
'''
