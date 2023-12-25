import uvicorn

from src.app.core.app.app import App
from src.app.core.app.request import Request
from src.app.core.app.response import Response
from src.app.core.app.route import Route
from src.app.internal.auth.transport.handlers import login, register
from src.app.internal.tasks.transport.handlers import (
    create_task,
    create_task_list,
    delete_task,
    delete_task_list,
    get_task,
    get_task_list,
    get_task_lists,
    get_tasks,
    update_task,
    update_task_list,
)
from src.app.internal.users.transport.handlers import create_user, delete_user, get_user, get_users, update_user
from src.config.settings import get_settings
from src.db.models import create_tables


async def root(request):
    return Response('Hello, World!')


async def hello(request: Request):
    return Response(f'Hello, {request.query_params}!')


settings = get_settings()

routes = [
    Route('/', root),
    Route('/hello', hello),
    Route('/api/auth/register', register, methods=['POST']),
    Route('/api/auth/login', login, methods=['POST']),
    Route('/api/users', create_user, methods=['POST']),
    Route('/api/users', get_users, methods=['GET']),
    Route('/api/users/{user_id:uuid}', get_user, methods=['GET']),
    Route('/api/users/{user_id:uuid}', update_user, methods=['PATCH']),
    Route('/api/users/{user_id:uuid}', delete_user, methods=['DELETE']),
    Route('/api/users/{user_id:uuid}/task_lists', create_task_list, methods=['POST']),
    Route('/api/users/{user_id:uuid}/task_lists', get_task_lists, methods=['GET']),
    Route('/api/users/{user_id:uuid}/task_lists/{task_list_id:uuid}', get_task_list, methods=['GET']),
    Route('/api/users/{user_id:uuid}/task_lists/{task_list_id:uuid}', update_task_list, methods=['PATCH']),
    Route('/api/users/{user_id:uuid}/task_lists/{task_list_id:uuid}', delete_task_list, methods=['DELETE']),
    Route('/api/users/{user_id:uuid}/task_lists/{task_list_id:uuid}/tasks', create_task, methods=['POST']),
    Route('/api/users/{user_id:uuid}/task_lists/{task_list_id:uuid}/tasks', get_tasks, methods=['GET']),
    Route('/api/users/{user_id:uuid}/task_lists/{task_list_id:uuid}/tasks/{task_id:uuid}', get_task, methods=['GET']),
    Route(
        '/api/users/{user_id:uuid}/task_lists/{task_list_id:uuid}/tasks/{task_id:uuid}', update_task, methods=['PATCH']
    ),
    Route(
        '/api/users/{user_id:uuid}/task_lists/{task_list_id:uuid}/tasks/{task_id:uuid}', delete_task, methods=['DELETE']
    ),
]

create_tables()

app = App(routes=routes)


if __name__ == '__main__':
    uvicorn.run('main:app', port=settings.APP_PORT, reload=True, log_level='debug')
