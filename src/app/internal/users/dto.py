import uuid

from pydantic import BaseModel


class UserCreateDTO(BaseModel):
    email: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False


class UserDTO(BaseModel):
    id: str
    email: str
    is_active: bool
    is_superuser: bool
    created_at: str
