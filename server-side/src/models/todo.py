from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func, text
from session import Base
from datetime import datetime, timedelta


class ToDo(Base):
    __tablename__ = 'todo'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    add_to_favourites: Mapped[bool] = mapped_column(default=False)
    completed: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    scheduled_for: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=text("(CURRENT_TIMESTAMP + interval '1 week')"))
    notification_sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    auto_updated: Mapped[bool] = mapped_column(default=False, nullable=False)

    def __repr__(self):
        return f"ToDo: {self.title}"

