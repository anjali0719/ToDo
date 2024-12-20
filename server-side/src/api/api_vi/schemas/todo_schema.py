from pydantic import BaseModel, Field

class CreateTodo(BaseModel):
    title: str = Field(min_length=3)
    description: str
    add_to_favourites: bool
    completed: bool
    # user_id: int

    class Config:
        orm_mode = True

