import uvicorn

from src.app.core.app.app import App
from src.app.core.app.response import Response
from src.app.core.app.route import Route


async def root(request):
    return Response('Hello, World!')


async def hello(request):
    return Response(f'Hello, {request}!')


routes = [Route('/', root), Route('/hello123', hello), ]
app = App(routes=routes)

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
