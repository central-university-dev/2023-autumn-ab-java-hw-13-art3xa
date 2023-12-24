from src.app.core.app.json_response import JSONResponse
from src.app.core.app.request import Request
from src.app.core.app.response import Response
from src.app.internal.auth.transport.di import get_auth_service
from src.app.internal.users.dto import UserRegisterDTO


async def register(request: Request) -> Response:
    user = await request.json()
    auth_service = get_auth_service()
    user_register_dto = UserRegisterDTO(email=user['email'], password=user['password'])
    error, tokens_dto = auth_service.register(user_register_dto)
    if error:
        return error
    return JSONResponse(tokens_dto.model_dump(), status_code=201)


async def login(request: Request) -> Response:
    user = await request.json()
    auth_service = get_auth_service()
    user_register_dto = UserRegisterDTO(email=user['email'], password=user['password'])
    error, tokens_dto = auth_service.login(user_register_dto)
    if error:
        return error
    return JSONResponse(tokens_dto.model_dump(), status_code=200)
