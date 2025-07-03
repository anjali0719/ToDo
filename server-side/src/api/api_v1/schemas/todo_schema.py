from datetime import datetime
from pydantic import BaseModel, Field
from fastapi_pagination import Page

class CreateOrUpdateTodo(BaseModel):
    title: str = Field(min_length=3)
    description: str
    add_to_favourites: bool
    completed: bool
    scheduled_for: datetime
    # user_id: int

    class Config:
        from_attributes = True

class ToDoResponse(BaseModel):
    id: int
    title: str
    description: str
    add_to_favourites: bool
    completed: bool
    scheduled_for: datetime

    class Config:
        from_attributes = True

class Counts(BaseModel):
    today: int
    upcoming: int
    favourites: int
    completed: int

class ToDoListResponse(BaseModel):
    counts: Counts
    results: Page[ToDoResponse]