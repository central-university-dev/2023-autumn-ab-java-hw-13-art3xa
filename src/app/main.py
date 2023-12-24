import uvicorn

from src.app.core.app.app import App
from src.app.core.app.request import Request
from src.app.core.app.response import Response
from src.app.core.app.route import Route
from src.app.internal.tasks.transport.handlers import create_task, delete_task, get_task, get_tasks
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

    Route('/api/tasks', get_tasks, methods=['GET']),
    Route('/api/tasks', create_task, methods=['POST']),
    Route('/api/tasks/{task_id:int}', get_task, methods=['GET']),
    Route('/api/tasks/{task_id:int}', delete_task, methods=['DELETE']),
]

create_tables()

app = App(routes=routes)


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=settings.APP_PORT, reload=True, log_level="debug")
