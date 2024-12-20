from fastapi import FastAPI
from session import Base, engine
from api.api_vi.routers import user_routes, todo_routes

app = FastAPI()
Base.metadata.create_all(engine)

app.include_router(user_routes.router)
app.include_router(todo_routes.router)
