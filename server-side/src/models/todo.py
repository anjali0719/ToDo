from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from session import Base


class ToDo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    add_to_favourites = Column(Boolean, default=False)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"ToDo: {self.title}"

