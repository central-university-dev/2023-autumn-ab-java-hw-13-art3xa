import uvicorn

from src.app.core.app.app import App
from src.app.core.app.request import Request
from src.app.core.app.response import Response
from src.app.core.app.route import Route
from src.app.internal.tasks.transport.handlers import create_task, get_task, get_tasks


async def root(request):
    return Response('Hello, World!')


async def hello(request: Request):
    return Response(f'Hello, {request.query_params}!')


routes = [
    Route('/', root),
    Route('/hello', hello),

    Route('/api/tasks', get_tasks, methods=['GET']),
    Route('/api/tasks', create_task, methods=['POST']),
    Route('/api/tasks/{task_id:uuid}', get_task, methods=['GET']),

]
app = App(routes=routes)

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
