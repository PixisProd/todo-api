from enum import Enum
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class OrmModel(DeclarativeBase):
    pass


class OrmUser(OrmModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    userlogin: Mapped[str] = mapped_column(String(12))
    userpassword: Mapped[str] = mapped_column(String(20))

class OrmTask(OrmModel):
    class TaskStatus(Enum):
        Done = "Done"
        Pending = "Pending"

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.Pending)