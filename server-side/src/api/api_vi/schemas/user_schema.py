from pydantic import BaseModel, Field

class CreateUser(BaseModel):
    first_name: str
    last_name: str
    password: str
    email: str

    class Config:
        orm_mode = True


class ChangePassword(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8)

    class Config:
        orm_mode = True

