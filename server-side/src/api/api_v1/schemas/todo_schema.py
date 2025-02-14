from datetime import datetime
from pydantic import BaseModel, Field

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
    title: str
    description: str

    class Config:
        from_attributes = True