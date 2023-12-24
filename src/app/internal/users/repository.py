from src.app.internal.users.dto import UserCreateDTO


class UserRepository:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def get_users(self):
        with self.db_conn.cursor() as cursor:
            cursor.execute("SELECT id, email, is_active, is_superuser, created_at FROM users")
            return cursor.fetchall()

    def create_user(self, user_id, user: UserCreateDTO) -> str:
        with self.db_conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (id, email, hashed_password, is_active, is_superuser) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
                (user_id, user.email, user.hashed_password, user.is_active, user.is_superuser)
            )
            self.db_conn.commit()
            return cursor.fetchone()[0]

    def get_user(self, user_id):
        with self.db_conn.cursor() as cursor:
            cursor.execute("SELECT id, email, is_active, is_superuser, created_at FROM users WHERE id = %s", (user_id,))
            return cursor.fetchone()

    def delete_user(self, user_id):
        with self.db_conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            self.db_conn.commit()
