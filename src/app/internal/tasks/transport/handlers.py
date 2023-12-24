
from src.app.core.app.json_response import JSONResponse
from src.app.core.app.request import Request
from src.app.core.app.response import Response
from src.app.internal.tasks.repository import TaskListRepository
from src.db.di import get_db


def get_task_list_repo():
    db_conn = get_db()
    return TaskListRepository(db_conn)


async def get_task_lists(request: Request) -> Response:
    task_list_repo = get_task_list_repo()
    user_id = str(request.path_params['user_id'])
    return JSONResponse(task_list_repo.get_task_lists())

async def create_task_list(request: Request) -> Response:
    task_list = await request.json()
    task_list_repo = get_task_list_repo()
    task_list['user_id'] = 12234
    task_list = task_list_repo.create_task_list(task_list['user_id'], task_list['title'], task_list['description'])
    return JSONResponse(task_list)


async def get_task(request: Request) -> Response:
    task_repo = get_task_list_repo()
    task_id = str(request.path_params['task_id'])
    task = task_repo.get_task(task_id)
    return JSONResponse(task)


async def get_tasks(request: Request) -> Response:
    task_repo = get_task_list_repo()
    return JSONResponse(task_repo.get_tasks())


async def create_task(request: Request) -> Response:
    task = await request.json()
    task_repo = get_task_list_repo()
    task['user_id'] = 12234
    task = task_repo.create_task(task['name'], task['description'], task['user_id'])
    return JSONResponse(task)


async def delete_task(request: Request) -> Response:
    task_repo = get_task_list_repo()
    task_id = str(request.path_params['task_id'])
    task_repo.delete_task(task_id)
    return Response(status_code=204)
