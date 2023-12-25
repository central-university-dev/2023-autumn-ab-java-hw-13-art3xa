import uuid

from src.app.core.app.exceptions import HTTPException
from src.app.core.app.json_response import JSONResponse
from src.app.core.app.request import Request
from src.app.core.app.response import Response
from src.app.internal.auth.hash import get_password_hash
from src.app.internal.auth.middlewares.service import get_current_user
from src.app.internal.users.dto import UserCreateDTO, UserUpdateDTO
from src.app.internal.users.transport.di import get_user_service


async def get_user(request: Request) -> Response:
    cur_user, error = await get_current_user(request)
    if error:
        return error
    user_service = get_user_service()
    user_id = str(request.path_params['user_id'])
    if not cur_user.is_superuser and cur_user.id != user_id:
        return HTTPException(status_code=403)
    user = user_service.get_user(user_id)
    if not user:
        return HTTPException('User not found', status_code=404)
    return JSONResponse(user)


async def get_users(request: Request) -> Response:
    cur_user, error = await get_current_user(request)
    if error:
        return error
    user_service = get_user_service()
    users = user_service.get_users()
    return JSONResponse(users)


async def create_user(request: Request) -> Response:
    user = await request.json()
    cur_user, error = await get_current_user(request)
    if error:
        return error
    user_service = get_user_service()
    user_db = user_service.get_by_email(user['email'])
    if user_db:
        return HTTPException('User already exists', status_code=400)
    user_id = str(uuid.uuid4())
    user_create_dto = UserCreateDTO(
        email=user['email'],
        hashed_password=get_password_hash(user['password']),
        is_active=user['is_active'],
        is_superuser=user['is_superuser'],
    )
    user_id = user_service.create_user(user_id, user_create_dto)
    return JSONResponse({'user_id': user_id}, status_code=201)


async def update_user(request: Request) -> Response:
    user_in = await request.json()
    cur_user, error = await get_current_user(request)
    if error:
        return error
    user_service = get_user_service()
    user_id = str(request.path_params['user_id'])
    if not cur_user.is_superuser and cur_user.id != user_id:
        return HTTPException(status_code=403)
    user = user_service.get_user(user_id)
    if not user:
        return HTTPException('User not found', status_code=404)
    user_update_dto = UserUpdateDTO(
        email=user_in['email'],
        hashed_password=get_password_hash(user_in['password']),
        is_active=user_in['is_active'],
        is_superuser=user_in['is_superuser'],
    )
    user_service.update_user(user_id, user_update_dto)
    updated_user = user_service.get_user(user_id)
    return JSONResponse(updated_user)


async def delete_user(request: Request) -> Response:
    cur_user, error = await get_current_user(request)
    if error:
        return error
    user_service = get_user_service()
    user_id = str(request.path_params['user_id'])
    user_service.delete_user(user_id)
    return Response(status_code=204)
