import uuid

from src.app.core.app.json_response import JSONResponse
from src.app.core.app.request import Request
from src.app.core.app.response import Response


dict_tasks = {
    str(uuid.uuid4()): {'name': 'test11111111', 'description': 'test1111111111111'},
}

async def get_task(request: Request) -> Response:
    task_id = str(request.path_params['task_id'])
    return JSONResponse(dict_tasks[task_id])


async def get_tasks(request: Request) -> Response:
    return JSONResponse(dict_tasks)


async def create_task(request: Request) -> Response:
    task = await request.json()
    task_id = str(uuid.uuid4())
    task['id'] = task_id
    dict_tasks[task_id] = task
    return JSONResponse(task)
