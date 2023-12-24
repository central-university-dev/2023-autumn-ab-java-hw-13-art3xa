import uvicorn

from src.app.core.app.app import App
from src.app.core.app.request import Request
from src.app.core.app.response import Response
from src.app.core.app.route import Route
from src.app.internal.tasks.transport.handlers import get_task


async def root(request):
    return Response('Hello, World!')


async def hello(request: Request):
    return Response(f'Hello, {request.query_params}!')


routes = [
    Route('/', root),
    Route('/hello123', hello),
    Route('/tasks/{task_id:int}', get_task),
]
app = App(routes=routes)

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
