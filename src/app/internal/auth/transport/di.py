from src.app.internal.auth.middlewares.auth import JWTAuth
from src.app.internal.auth.repository import JWTTokenRepository
from src.app.internal.auth.service import AuthService
from src.app.internal.users.repository import UserRepository
from src.config.settings import get_settings
from src.db.di import get_db


def get_auth_service() -> AuthService:
    db_conn = get_db()
    user_repo = UserRepository(db_conn)
    jwt_token_repo = JWTTokenRepository(db_conn)
    jwt_auth = JWTAuth(config=get_settings().jwt_config)
    return AuthService(user_repo=user_repo, jwt_token_repo=jwt_token_repo, jwt_auth=jwt_auth)
