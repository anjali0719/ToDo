from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    password: str
    email: str

    class Config:
        orm_mode = True

