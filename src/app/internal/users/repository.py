class UserRepository:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def get_users(self):
        with self.db_conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            return cursor.fetchall()

    def create_user(self, email, hashed_password, is_active, is_superuser):
        with self.db_conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (email, hashed_password, is_active, is_superuser) VALUES (%s, %s, %s, %s) RETURNING id;",
                (email, hashed_password, is_active, is_superuser)
            )
            self.db_conn.commit()
            return cursor.fetchone()[0]

    def get_user(self, user_id):
        with self.db_conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            return cursor.fetchone()

    def delete_user(self, user_id):
        with self.db_conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            self.db_conn.commit()

    def get_user_by_email(self, email):
        with self.db_conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            return cursor.fetchone()
