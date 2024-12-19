from fastapi import FastAPI, Depends
from session import get_db, Base, engine
from sqlalchemy.orm import Session
from api.api_vi.routers import user_routes

app = FastAPI()
Base.metadata.create_all(engine)

app.include_router(user_routes.router)

