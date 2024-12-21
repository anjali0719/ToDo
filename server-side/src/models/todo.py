from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from session import Base


class ToDo(Base):
    __tablename__ = 'todo'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    add_to_favourites: Mapped[bool] = mapped_column(default=False)
    completed: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"ToDo: {self.title}"

