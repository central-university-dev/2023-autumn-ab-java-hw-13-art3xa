from src.app.core.app.json_response import JSONResponse
from src.app.core.app.request import Request
from src.app.core.app.response import Response


async def get_task(request: Request) -> Response:
    task = {'id': 1, 'name': 'test', 'description': 'test'}
    return JSONResponse(task)
