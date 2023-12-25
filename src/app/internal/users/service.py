from src.app.internal.users.dto import UserCreateDTO, UserDTO, UserFullDTO, UserUpdateDTO
from src.app.internal.users.repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_users(self) -> list[UserDTO]:
        users = self.user_repo.get_users()
        users_dto = []
        for user in users:
            user_dto = UserDTO(
                id=user[0], email=user[1], is_active=user[2], is_superuser=user[3], created_at=user[4].isoformat()
            )
            users_dto.append(user_dto.model_dump())
        return users_dto

    def get_user(self, user_id: str) -> UserDTO | None:
        user = self.user_repo.get_user(user_id)
        if not user:
            return None
        user_dto = UserDTO(
            id=user[0], email=user[1], is_active=user[2], is_superuser=user[3], created_at=user[4].isoformat()
        )
        return user_dto.model_dump()

    def create_user(self, user_id: str, user: UserCreateDTO) -> str:
        user_id = self.user_repo.create_user(user_id, user)
        return user_id

    def update_user(self, user_id: str, user: UserUpdateDTO) -> None:
        self.user_repo.update_user(user_id, user)

    def delete_user(self, user_id: str) -> None:
        self.user_repo.delete_user(user_id)

    def get_by_email(self, email: str) -> UserFullDTO | None:
        user = self.user_repo.get_by_email(email)
        if not user:
            return None
        user_dto = UserFullDTO(
            id=user[0],
            email=user[1],
            hashed_password=user[2],
            is_active=user[3],
            is_superuser=user[4],
            created_at=user[5].isoformat(),
        )
        return user_dto.model_dump()
