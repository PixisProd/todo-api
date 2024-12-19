from pydantic import BaseModel
from orm_models import OrmTask


class PUser(BaseModel):
    userlogin: str
    userpassword: str


class PTask(BaseModel):
    title: str
    description: str | None = None
    status: OrmTask.TaskStatus


class PTaskEdit(BaseModel):
    title: str | None = None
    description: str | None = None
    status: OrmTask.TaskStatus