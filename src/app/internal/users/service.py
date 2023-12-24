from src.app.internal.users.repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, email, hashed_password, is_active, is_superuser):
        return self.user_repo.create_user(email, hashed_password, is_active, is_superuser)