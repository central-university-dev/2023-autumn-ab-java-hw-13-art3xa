import base64


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return base64.b64encode(plain_password.encode()).decode() == hashed_password


def get_password_hash(password: str) -> str:
    return base64.b64encode(password.encode()).decode()
