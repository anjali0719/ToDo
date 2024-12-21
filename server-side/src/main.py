from fastapi import FastAPI
from session import Base, engine
from api.api_v1.routers import user_routes, todo_routes

app = FastAPI()
Base.metadata.create_all(engine)

app.include_router(user_routes.router)
app.include_router(todo_routes.router)


# TO BE IMPLEMENETED:
'''
1. Use Mapped and mapped_column instead of Column
2. Use alembic and make changes to ToDo model: add created_at and updated_at fields
3. Handle exceptions/errors for all the created routers
'''
