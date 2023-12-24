from pydantic import BaseModel


class UserDTO(BaseModel):
    id: str
    email: str
    is_active: bool
    is_superuser: bool
    created_at: str


class UserCreateDTO(BaseModel):
    email: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False


class UserUpdateDTO(BaseModel):
    email: str | None = None
    hashed_password: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None


class UserRegisterDTO(BaseModel):
    email: str
    password: str


class UserFullDTO(BaseModel):
    id: str
    email: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
    created_at: str
