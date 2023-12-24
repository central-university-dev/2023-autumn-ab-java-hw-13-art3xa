import uuid

from src.app.core.app.response import Response
from src.app.internal.auth.dto import JWTTokenCreateDTO, TokensDTO
from src.app.internal.auth.hash import get_password_hash, verify_password
from src.app.internal.auth.middlewares.auth import JWTAuth
from src.app.internal.auth.repository import JWTTokenRepository
from src.app.internal.auth.utils import generate_device_id
from src.app.internal.users.dto import UserCreateDTO, UserFullDTO, UserRegisterDTO
from src.app.internal.users.repository import UserRepository


class AuthService:
    def __init__(self, user_repo: UserRepository, jwt_token_repo: JWTTokenRepository, jwt_auth: JWTAuth) -> None:
        self.user_repo = user_repo
        self.jwt_token_repo = jwt_token_repo
        self.jwt_auth = jwt_auth

    def register(self, user_dto: UserRegisterDTO) -> Response | TokensDTO:
        if self.user_repo.get_by_email(email=user_dto.email):
            return Response(
                status_code=400, content='Account already exists', headers={'WWW-Authenticate': 'Bearer'}
            ), None
        user_create = UserCreateDTO(email=user_dto.email, hashed_password=get_password_hash(user_dto.password))
        user_id = str(uuid.uuid4())
        user_id = self.user_repo.create_user(user_id, user_create)

        return None, self._issue_tokens(user_id=user_id)

    def login(self, user_dto: UserRegisterDTO) -> Response | TokensDTO:
        user_data = self.user_repo.get_by_email(email=user_dto.email)
        if not user_data:
            return Response(status_code=400, content='User not found', headers={'WWW-Authenticate': 'Bearer'}), None
        user = UserFullDTO(
            id=user_data[0],
            email=user_data[1],
            hashed_password=user_data[2],
            is_active=user_data[3],
            is_superuser=user_data[4],
            created_at=user_data[5].isoformat(),
        )
        if not verify_password(user_dto.password, user.hashed_password):
            return Response(status_code=400, content='Incorrect password', headers={'WWW-Authenticate': 'Bearer'}), None

        return None, self._issue_tokens(user_id=user.id)

    async def logout(self, user_id: str, device_id: str) -> None:
        self.jwt_token_repo.update_by_user_id_and_device_id(user_id=user_id, device_id=device_id, is_blacklisted=True)

    def _issue_tokens(self, user_id: str, device_id: str = generate_device_id()) -> TokensDTO:
        tokens = self.jwt_auth.generate_tokens(subject=user_id, payload={'device_id': device_id})

        raw_jwt_tokens = [self.jwt_auth.decode_token(token) for token in (tokens.access_token, tokens.refresh_token)]

        for raw_jwt_token in raw_jwt_tokens:
            jwt_token = JWTTokenCreateDTO(user_id=user_id, jti=raw_jwt_token.get('jti'), device_id=device_id)
            self.jwt_token_repo.create_jwt_token(jwt_token)

        return tokens
