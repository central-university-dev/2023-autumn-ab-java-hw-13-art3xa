class TaskRepository:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def get_tasks(self):
        with self.db_conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tasks")
            return cursor.fetchall()

    def create_task(self, name, description, user_id):
        with self.db_conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO tasks (name, description, user_id) VALUES (%s, %s, %s) RETURNING id;",
                (name, description, user_id)
            )
            self.db_conn.commit()
            return cursor.fetchone()[0]

    def get_task(self, task_id):
        with self.db_conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
            return cursor.fetchone()

    def delete_task(self, task_id):
        with self.db_conn.cursor() as cursor:
            cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            self.db_conn.commit()

