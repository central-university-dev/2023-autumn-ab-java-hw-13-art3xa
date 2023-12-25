import uuid

from src.app.core.app.exceptions import HTTPException
from src.app.core.app.json_response import JSONResponse
from src.app.core.app.request import Request
from src.app.core.app.response import Response
from src.app.internal.auth.middlewares.service import get_current_user
from src.app.internal.tasks.dto import (
    TaskCreateDTO,
    TaskListCreateDTO,
    TaskListUpdateDTO,
    TaskUpdateDTO,
)
from src.app.internal.tasks.transport.di import get_task_list_service


async def get_task_lists(request: Request) -> Response:
    cur_user, error = await get_current_user(request)
    if error:
        return error
    task_list_service = get_task_list_service()
    user_id = str(request.path_params['user_id'])
    if not cur_user.is_superuser and cur_user.id != user_id:
        return HTTPException(status_code=403)
    task_lists = task_list_service.get_task_lists(user_id)
    return JSONResponse(task_lists)


async def get_task_list(request: Request) -> Response:
    cur_user, error = await get_current_user(request)
    if error:
        return error
    task_list_service = get_task_list_service()
    user_id = str(request.path_params['user_id'])
    if not cur_user.is_superuser and cur_user.id != user_id:
        return HTTPException(status_code=403)
    task_list_id = str(request.path_params['task_list_id'])
    task_list = task_list_service.get_task_list(user_id, task_list_id)
    if not task_list:
        return HTTPException('Task list not found', status_code=404)
    return JSONResponse(task_list)


async def create_task_list(request: Request) -> Response:
    task_list = await request.json()
    cur_user, error = await get_current_user(request)
    if error:
        return error
    task_list_service = get_task_list_service()
    user_id = str(request.path_params['user_id'])
    if not cur_user.is_superuser and cur_user.id != user_id:
        return HTTPException(status_code=403)
    task_list_id = str(uuid.uuid4())
    task_list_create_dto = TaskListCreateDTO(title=task_list['title'], description=task_list['description'])
    task_list_id = task_list_service.create_task_list(task_list_id, task_list_create_dto)
    return JSONResponse({'task_list_id': task_list_id})


async def update_task_list(request: Request) -> Response:
    task_list = await request.json()
    cur_user, error = await get_current_user(request)
    if error:
        return error
    task_list_service = get_task_list_service()
    user_id = str(request.path_params['user_id'])
    if not cur_user.is_superuser and cur_user.id != user_id:
        return HTTPException(status_code=403)
    task_list_id = str(request.path_params['task_list_id'])
    task_list_update_dto = TaskListUpdateDTO(title=task_list['title'], description=task_list['description'])
    task_list_service.update_task_list(user_id, task_list_id, task_list_update_dto)
    task_list = task_list_service.get_task_list(user_id, task_list_id)
    return JSONResponse(task_list)


async def delete_task_list(request: Request) -> Response:
    cur_user, error = await get_current_user(request)
    if error:
        return error
    task_list_service = get_task_list_service()
    task_list_id = str(request.path_params['task_list_id'])
    user_id = str(request.path_params['user_id'])
    if not cur_user.is_superuser and cur_user.id != user_id:
        return HTTPException(status_code=403)
    task_list_service.delete_task_list(user_id, task_list_id)
    return Response(status_code=204)


async def get_task(request: Request) -> Response:
    cur_user, error = await get_current_user(request)
    if error:
        return error
    task_list_service = get_task_list_service()
    task_list_id = str(request.path_params['task_list_id'])
    user_id = str(request.path_params['user_id'])
    task_id = str(request.path_params['task_id'])
    if not cur_user.is_superuser and cur_user.id != user_id:
        return HTTPException(status_code=403)
    task_list = task_list_service.get_task_list(user_id, task_list_id)
    task = task_list_service.get_task(task_id)
    if not task or task.id not in [task.id for task in task_list.tasks]:
        return HTTPException('Task not found', status_code=404)
    return JSONResponse(task.model_dump())


async def get_tasks(request: Request) -> Response:
    cur_user, error = await get_current_user(request)
    if error:
        return error
    task_list_service = get_task_list_service()
    task_list_id = str(request.path_params['task_list_id'])
    user_id = str(request.path_params['user_id'])
    if not cur_user.is_superuser and cur_user.id != user_id:
        return HTTPException(status_code=403)
    task_list = task_list_service.get_task_list(user_id, task_list_id)
    if not task_list:
        return HTTPException('Task list not found', status_code=404)
    tasks = task_list_service.get_tasks(task_list_id)
    return JSONResponse(tasks)


async def create_task(request: Request) -> Response:
    task = await request.json()
    cur_user, error = await get_current_user(request)
    if error:
        return error
    task_list_service = get_task_list_service()
    task_list_id = str(request.path_params['task_list_id'])
    user_id = str(request.path_params['user_id'])
    if not cur_user.is_superuser and cur_user.id != user_id:
        return HTTPException(status_code=403)
    task_list = task_list_service.get_task_list(user_id, task_list_id)
    if not task_list:
        return HTTPException('Task list not found', status_code=404)
    task_id = str(uuid.uuid4())
    task_create_dto = TaskCreateDTO(
        task_list_id=task_list_id, title=task['title'], description=task['description'], due_date=task['due_date']
    )
    task_id = task_list_service.create_task(task_id, task_create_dto)
    return JSONResponse({'task_id': task_id})


async def update_task(request: Request) -> Response:
    task_in = await request.json()
    cur_user, error = await get_current_user(request)
    if error:
        return error
    task_list_service = get_task_list_service()
    task_list_id = str(request.path_params['task_list_id'])
    user_id = str(request.path_params['user_id'])
    task_id = str(request.path_params['task_id'])
    if not cur_user.is_superuser and cur_user.id != user_id:
        return HTTPException(status_code=403)
    task_list = task_list_service.get_task_list(user_id, task_list_id)
    if not task_list:
        return HTTPException('Task list not found', status_code=404)
    task = task_list_service.get_task(task_id)
    if not task or task.id not in [task.id for task in task_list.tasks]:
        return HTTPException('Task not found', status_code=404)
    task_update_dto = TaskUpdateDTO(
        title=task_in['title'],
        description=task_in['description'],
        due_date=task_in['due_date'],
        completed=task_in['completed'],
    )
    task_list_service.update_task(task_id, task_update_dto)
    updated_task = task_list_service.get_task(task_id)
    return JSONResponse(updated_task)


async def delete_task(request: Request) -> Response:
    cur_user, error = await get_current_user(request)
    if error:
        return error
    task_list_service = get_task_list_service()
    task_list_id = str(request.path_params['task_list_id'])
    user_id = str(request.path_params['user_id'])
    task_id = str(request.path_params['task_id'])
    if not cur_user.is_superuser and cur_user.id != user_id:
        return HTTPException(status_code=403)
    task_list = task_list_service.get_task_list(user_id, task_list_id)
    if not task_list:
        return HTTPException('Task list not found', status_code=404)
    task = task_list_service.get_task(task_id)
    if not task or task.id not in [task.id for task in task_list.tasks]:
        return HTTPException('Task not found', status_code=404)
    task_list_service.delete_task(task_id)
    return Response(status_code=204)
