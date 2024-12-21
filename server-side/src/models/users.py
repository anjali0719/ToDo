from sqlalchemy.orm import Mapped, mapped_column

from session import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    hashed_password: Mapped[str] = mapped_column()


    def __repr__(self):
        return f"User: {self.first_name} {self.last_name}".strip()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
