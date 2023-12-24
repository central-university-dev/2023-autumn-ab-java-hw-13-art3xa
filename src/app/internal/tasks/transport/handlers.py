import uuid

from src.app.core.app.json_response import JSONResponse
from src.app.core.app.request import Request
from src.app.core.app.response import Response
from src.app.internal.tasks.dto import (
    TaskCreateDTO,
    TaskListCreateDTO,
    TaskListUpdateDTO,
    TaskUpdateDTO,
)
from src.app.internal.tasks.transport.di import get_task_list_service


async def get_task_lists(request: Request) -> Response:
    task_list_service = get_task_list_service()
    user_id = str(request.path_params['user_id'])
    task_lists = task_list_service.get_task_lists(user_id)
    return JSONResponse(task_lists)


async def get_task_list(request: Request) -> Response:
    task_list_service = get_task_list_service()
    user_id = str(request.path_params['user_id'])
    task_list_id = str(request.path_params['task_list_id'])
    task_list = task_list_service.get_task_list(user_id, task_list_id)
    if not task_list:
        return Response('Task list not found', status_code=404)
    return JSONResponse(task_list)


async def create_task_list(request: Request) -> Response:
    task_list = await request.json()
    task_list_service = get_task_list_service()
    user_id = str(request.path_params['user_id'])
    task_list_id = str(uuid.uuid4())
    task_list_create_dto = TaskListCreateDTO(
        user_id=user_id, title=task_list['title'], description=task_list['description']
    )
    task_list_id = task_list_service.create_task_list(task_list_id, task_list_create_dto)
    return JSONResponse({'task_list_id': task_list_id})


async def update_task_list(request: Request) -> Response:
    task_list = await request.json()
    task_list_service = get_task_list_service()
    user_id = str(request.path_params['user_id'])
    task_list_id = str(request.path_params['task_list_id'])
    task_list_update_dto = TaskListUpdateDTO(title=task_list['title'], description=task_list['description'])
    task_list_service.update_task_list(user_id, task_list_id, task_list_update_dto)
    task_list = task_list_service.get_task_list(user_id, task_list_id)
    return JSONResponse(task_list)


async def delete_task_list(request: Request) -> Response:
    task_list_service = get_task_list_service()
    task_list_id = str(request.path_params['task_list_id'])
    user_id = str(request.path_params['user_id'])
    task_list_service.delete_task_list(user_id, task_list_id)
    return Response(status_code=204)


async def get_task(request: Request) -> Response:
    task_list_service = get_task_list_service()
    task_id = str(request.path_params['task_id'])
    task = task_list_service.get_task(task_id)
    if not task:
        return Response('Task not found', status_code=404)
    return JSONResponse(task)


async def get_tasks(request: Request) -> Response:
    task_list_service = get_task_list_service()
    task_list_id = str(request.path_params['task_list_id'])
    tasks = task_list_service.get_tasks(task_list_id)
    return JSONResponse(tasks)


async def create_task(request: Request) -> Response:
    task = await request.json()
    task_list_service = get_task_list_service()
    task_list_id = str(request.path_params['task_list_id'])
    task_id = str(uuid.uuid4())
    task_create_dto = TaskCreateDTO(
        task_list_id=task_list_id, title=task['title'], description=task['description'], due_date=task['due_date']
    )
    task_id = task_list_service.create_task(task_id, task_create_dto)
    return JSONResponse({'task_id': task_id})


async def update_task(request: Request) -> Response:
    task = await request.json()
    task_list_service = get_task_list_service()
    task_id = str(request.path_params['task_id'])
    task_update_dto = TaskUpdateDTO(
        title=task['title'], description=task['description'], due_date=task['due_date'], completed=task['completed']
    )
    task_list_service.update_task(task_id, task_update_dto)
    task = task_list_service.get_task(task_id)
    return JSONResponse(task)


async def delete_task(request: Request) -> Response:
    task_list_service = get_task_list_service()
    task_id = str(request.path_params['task_id'])
    task_list_service.delete_task(task_id)
    return Response(status_code=204)
