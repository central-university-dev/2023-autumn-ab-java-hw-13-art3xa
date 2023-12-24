import uuid

from pydantic import BaseModel


class TaskListCreateDTO(BaseModel):
    user_id: uuid.UUID
    title: str
    description: str


class TaskListUpdateDTO(BaseModel):
    id: uuid.UUID | None = None
    user_id: uuid.UUID | None = None
    title: str | None = None
    description: str | None = None


class TaskListDTO(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    description: str
    tasks: list