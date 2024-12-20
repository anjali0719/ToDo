from sqlalchemy import Column, String, Boolean, Integer

from session import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String)


    def __repr__(self):
        return f"User: {self.first_name} {self.last_name}".strip()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
