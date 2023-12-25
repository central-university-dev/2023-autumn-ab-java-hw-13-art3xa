from src.app.internal.users.repository import UserRepository
from src.app.internal.users.service import UserService
from src.db.di import get_db


def get_user_service() -> UserService:
    db_conn = get_db()
    user_repo = UserRepository(db_conn)
    return UserService(user_repo)
