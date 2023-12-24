from pydantic import BaseModel


class TokensDTO(BaseModel):
    access_token: str
    refresh_token: str


class JWTTokenCreateDTO(BaseModel):
    jti: str
    is_blacklisted: bool = False
    user_id: str
    device_id: str


class JWTTokenUpdateDTO(BaseModel):
    user_id: str | None = None
    jti: str | None = None
    device_id: str | None = None


class JWTTokenDTO(BaseModel):
    jti: str
    is_blacklisted: bool
    user_id: str
    device_id: str
