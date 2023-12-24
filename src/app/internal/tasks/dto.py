from pydantic import BaseModel


class TaskDTO(BaseModel):
    id: str
    title: str
    description: str
    due_date: str
    completed: bool
    created_at: str


class TaskCreateDTO(BaseModel):
    task_list_id: str
    title: str
    description: str
    due_date: str


class TaskUpdateDTO(BaseModel):
    title: str | None = None
    description: str | None = None
    due_date: str | None = None
    completed: bool | None = None


class TaskListDTO(BaseModel):
    id: str
    title: str
    description: str
    created_at: str
    tasks: list[TaskDTO]


class TaskListCreateDTO(BaseModel):
    user_id: str
    title: str
    description: str


class TaskListUpdateDTO(BaseModel):
    title: str | None = None
    description: str | None = None
