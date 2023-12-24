import uuid

from src.app.core.app.json_response import JSONResponse
from src.app.core.app.request import Request
from src.app.core.app.response import Response
from src.app.internal.tasks.dto import (
    TaskCreateDTO, TaskDTO, TaskListCreateDTO, TaskListDTO, TaskListUpdateDTO, TaskUpdateDTO,
)
from src.app.internal.tasks.repository import TaskListRepository
from src.db.di import get_db


def get_task_list_repo():
    db_conn = get_db()
    return TaskListRepository(db_conn)


async def get_task_lists(request: Request) -> Response:
    task_list_repo = get_task_list_repo()
    user_id = str(request.path_params['user_id'])
    task_lists = task_list_repo.get_task_lists(user_id)
    task_lists_dto = []
    for task_list in task_lists:
        tasks_dto = []
        for task in task_list['tasks']:
            task_dto = TaskDTO(id=task['id'], title=task['title'], description=task['description'],
                due_date=task['due_date'].isoformat(), completed=task['completed'],
                created_at=task['created_at'].isoformat())
            tasks_dto.append(task_dto)
        task_list_dto = TaskListDTO(id=task_list['id'], title=task_list['title'], description=task_list['description'],
            created_at=task_list['created_at'].isoformat(), tasks=tasks_dto)
        task_lists_dto.append(task_list_dto.model_dump())

    return JSONResponse(task_lists_dto)


async def get_task_list(request: Request) -> Response:
    task_list_repo = get_task_list_repo()
    task_list_id = str(request.path_params['task_list_id'])
    user_id = str(request.path_params['user_id'])
    task_list = task_list_repo.get_task_list(user_id, task_list_id)
    if not task_list:
        return Response("Task list not found", status_code=404)
    tasks_dto = []
    for task in task_list['tasks']:
        task_dto = TaskDTO(id=task['id'], title=task['title'], description=task['description'],
            due_date=task['due_date'].isoformat(), completed=task['completed'],
            created_at=task['created_at'].isoformat())
        tasks_dto.append(task_dto)
    task_list_dto = TaskListDTO(id=task_list['id'], title=task_list['title'], description=task_list['description'],
        created_at=task_list['created_at'].isoformat(), tasks=tasks_dto)
    return JSONResponse(task_list_dto.model_dump())


async def create_task_list(request: Request) -> Response:
    task_list = await request.json()
    task_list_repo = get_task_list_repo()
    user_id = str(request.path_params['user_id'])
    task_list_id = str(uuid.uuid4())
    task_list_create_dto = TaskListCreateDTO(user_id=user_id, title=task_list['title'],
        description=task_list['description'])
    task_list_id = task_list_repo.create_task_list(task_list_id, task_list_create_dto)
    return JSONResponse({"task_list_id": task_list_id})


async def update_task_list(request: Request) -> Response:
    task_list = await request.json()
    task_list_repo = get_task_list_repo()
    task_list_id = str(request.path_params['task_list_id'])
    user_id = str(request.path_params['user_id'])
    task_list_update_dto = TaskListUpdateDTO(title=task_list['title'], description=task_list['description'])
    task_list_repo.update_task_list(user_id, task_list_id, task_list_update_dto)
    return Response(status_code=204)


async def delete_task_list(request: Request) -> Response:
    task_list_repo = get_task_list_repo()
    task_list_id = str(request.path_params['task_list_id'])
    user_id = str(request.path_params['user_id'])
    task_list_repo.delete_task_list(user_id, task_list_id)
    return Response(status_code=204)


async def get_task(request: Request) -> Response:
    task_list_repo = get_task_list_repo()
    task_id = str(request.path_params['task_id'])
    task = task_list_repo.get_task(task_id)
    if not task:
        return Response("Task not found", status_code=404)
    task_dto = TaskDTO(id=task[0], title=task[1], description=task[2], due_date=task[3].isoformat(), completed=task[4],
        created_at=task[5].isoformat())
    return JSONResponse(task_dto.model_dump())


async def get_tasks(request: Request) -> Response:
    task_list_repo = get_task_list_repo()
    task_list_id = str(request.path_params['task_list_id'])
    tasks = task_list_repo.get_tasks(task_list_id)
    tasks_dto = []
    for task in tasks:
        task_dto = TaskDTO(id=task[0], title=task[1], description=task[2], due_date=task[3].isoformat(),
            completed=task[4], created_at=task[5].isoformat())
        tasks_dto.append(task_dto.model_dump())
    return JSONResponse(tasks_dto)


async def create_task(request: Request) -> Response:
    task = await request.json()
    task_repo = get_task_list_repo()
    task_list_id = str(request.path_params['task_list_id'])
    task_id = str(uuid.uuid4())
    task_create_dto = TaskCreateDTO(task_list_id=task_list_id, title=task['title'], description=task['description'],
        due_date=task['due_date'])
    task_id = task_repo.create_task(task_id, task_create_dto)
    return JSONResponse({"task_id": task_id})


async def update_task(request: Request) -> Response:
    task = await request.json()
    task_repo = get_task_list_repo()
    task_id = str(request.path_params['task_id'])
    task_update_dto = TaskUpdateDTO(title=task['title'], description=task['description'], due_date=task['due_date'],
        completed=task['completed'])
    task_repo.update_task(task_id, task_update_dto)
    return Response(status_code=204)


async def delete_task(request: Request) -> Response:
    task_repo = get_task_list_repo()
    task_id = str(request.path_params['task_id'])
    task_repo.delete_task(task_id)
    return Response(status_code=204)
