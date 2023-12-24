import base64
import uuid

from src.app.core.app.json_response import JSONResponse
from src.app.core.app.request import Request
from src.app.core.app.response import Response
from src.app.internal.users.dto import UserCreateDTO, UserDTO
from src.app.internal.users.repository import UserRepository
from src.db.di import get_db


def get_password_hash(password: str) -> str:
    return base64.b64encode(password.encode()).decode()


def get_user_repo():
    db_conn = get_db()
    return UserRepository(db_conn)


async def get_user(request: Request) -> Response:
    user_repo = get_user_repo()
    user_id = str(request.path_params['user_id'])
    user = user_repo.get_user(user_id)
    if not user:
        return Response("User not found", status_code=404)
    user_dto = UserDTO(
        id=user[0],
        email=user[1],
        is_active=user[2],
        is_superuser=user[3],
        created_at=user[4].isoformat()
    )
    return JSONResponse(user_dto.model_dump())


async def get_users(request: Request) -> Response:
    user_repo = get_user_repo()
    users = user_repo.get_users()
    users_dto = []
    for user in users:
        user_dto = UserDTO(
            id=user[0],
            email=user[1],
            is_active=user[2],
            is_superuser=user[3],
            created_at=user[4].isoformat()
        )
        users_dto.append(user_dto.model_dump())
    return JSONResponse(users_dto)


async def create_user(request: Request) -> Response:
    user = await request.json()
    user_repo = get_user_repo()
    user_id = str(uuid.uuid4())
    user_create_dto = UserCreateDTO(
        email=user['email'],
        hashed_password=get_password_hash(user['password']),
        is_active=user['is_active'],
        is_superuser=user['is_superuser']
    )
    user_id = user_repo.create_user(user_id, user_create_dto)
    return JSONResponse({"user_id": user_id}, status_code=201)


async def delete_user(request: Request) -> Response:
    user_repo = get_user_repo()
    user_id = str(request.path_params['user_id'])
    user_repo.delete_user(user_id)
    return Response(status_code=204)

