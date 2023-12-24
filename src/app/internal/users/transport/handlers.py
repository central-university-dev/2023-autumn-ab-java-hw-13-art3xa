import base64
import uuid

from src.app.core.app.json_response import JSONResponse
from src.app.core.app.request import Request
from src.app.core.app.response import Response
from src.app.internal.users.dto import UserCreateDTO, UserUpdateDTO
from src.app.internal.users.repository import UserRepository
from src.app.internal.users.service import UserService
from src.db.di import get_db


def get_password_hash(password: str) -> str:
    return base64.b64encode(password.encode()).decode()


def get_user_service():
    db_conn = get_db()
    user_repo = UserRepository(db_conn)
    return UserService(user_repo)


async def get_user(request: Request) -> Response:
    user_service = get_user_service()
    user_id = str(request.path_params['user_id'])
    user = user_service.get_user(user_id)
    if not user:
        return Response('User not found', status_code=404)
    return JSONResponse(user)


async def get_users(request: Request) -> Response:
    user_service = get_user_service()
    users = user_service.get_users()
    return JSONResponse(users)


async def create_user(request: Request) -> Response:
    user = await request.json()
    user_service = get_user_service()
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
    user = await request.json()
    user_service = get_user_service()
    user_id = str(request.path_params['user_id'])
    user_update_dto = UserUpdateDTO(
        email=user['email'],
        hashed_password=get_password_hash(user['password']),
        is_active=user['is_active'],
        is_superuser=user['is_superuser'],
    )
    user_service.update_user(user_id, user_update_dto)
    user = user_service.get_user(user_id)
    return JSONResponse(user)


async def delete_user(request: Request) -> Response:
    user_service = get_user_service()
    user_id = str(request.path_params['user_id'])
    user_service.delete_user(user_id)
    return Response(status_code=204)
