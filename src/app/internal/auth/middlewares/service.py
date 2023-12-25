from jose import jwt

from src.app.core.app.exceptions import HTTPException
from src.app.core.app.request import Request
from src.app.internal.auth.middlewares.auth import TokenType
from src.app.internal.auth.repository import JWTTokenRepository
from src.app.internal.users.dto import UserDTO
from src.app.internal.users.repository import UserRepository
from src.config.settings import get_settings
from src.db.di import get_db


def get_user_repo() -> UserRepository:
    return UserRepository(get_db())


def get_jwt_token_repo() -> JWTTokenRepository:
    return JWTTokenRepository(get_db())


async def get_current_user(request: Request) -> UserDTO | HTTPException:
    authorization = request.headers.get('Authorization')
    scheme, token = authorization.split() if authorization else ('', '')
    if not authorization or scheme.lower() != 'bearer' or not token:
        return None, HTTPException('Not authenticated', status_code=401, headers={'WWW-Authenticate': 'Bearer'})
    try:
        payload = jwt.decode(
            token, get_settings().jwt_config.secret_key, algorithms=[get_settings().jwt_config.algorithm]
        )
        if payload.get('type') != TokenType.ACCESS.value:
            return None, HTTPException('The passed token does not match the required type', status_code=403)
    except jwt.JWTError:
        return None, HTTPException('The transferred token is invalid', status_code=403)

    jwt_token_repo = get_jwt_token_repo()
    jwt_token = jwt_token_repo.get_by_jti(payload.get('jti'))
    if jwt_token[1]:
        return None, HTTPException('The transferred token is blacklisted', status_code=403)

    user_repo = get_user_repo()
    user_data = user_repo.get_user(payload.get('sub'))
    if not user_data:
        return None, HTTPException('The owner of this access token has not been found', status_code=403)

    request.scope['device_id'] = payload.get('device_id')
    user_dto = UserDTO(
        id=user_data[0],
        email=user_data[1],
        is_active=user_data[2],
        is_superuser=user_data[3],
        created_at=user_data[4].isoformat(),
    )
    return user_dto, None
