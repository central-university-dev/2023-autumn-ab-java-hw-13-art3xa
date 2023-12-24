from src.app.internal.auth.dto import JWTTokenCreateDTO


class JWTTokenRepository:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def get_by_jti(self, jti: str):
        query = """
            SELECT jti, is_blacklisted, user_id, device_id
            FROM jwt_tokens
            WHERE jti = %s
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(query, (jti,))
            return cursor.fetchone()

    def update_by_user_id(self, user_id: str, is_blacklisted: bool) -> None:
        query = """
            UPDATE jwt_tokens
            SET is_blacklisted = %s
            WHERE user_id = %s
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(query, (is_blacklisted, user_id))
            self.db_conn.commit()

    def update_by_user_id_and_device_id(self, user_id: str, device_id: str, is_blacklisted: bool) -> None:
        query = """
            UPDATE jwt_tokens
            SET is_blacklisted = %s
            WHERE user_id = %s AND device_id = %s
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(query, (is_blacklisted, user_id, device_id))
            self.db_conn.commit()

    def create_jwt_token(self, jwt_token: JWTTokenCreateDTO) -> None:
        query = """
            INSERT INTO jwt_tokens (jti, is_blacklisted, user_id, device_id)
            VALUES (%s, %s, %s, %s)
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(query, (jwt_token.jti, jwt_token.is_blacklisted, jwt_token.user_id, jwt_token.device_id))
            self.db_conn.commit()
