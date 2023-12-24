class TaskListRepository:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def create_task_list(self, user_id, title, description):
        query = """
            INSERT INTO task_lists (user_id, title, description) 
            VALUES (%s, %s, %s) 
            RETURNING id
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(query, (user_id, title, description))
            task_list_id = cursor.fetchone()[0]
        self.db_conn.commit()
        return task_list_id

    def get_task_lists(self, user_id):
        query = """
            SELECT tl.id AS task_list_id,
               tl.title AS task_list_title,
               tl.description AS task_list_description,
               tl.created_at AS task_list_created_at,
               t.id AS task_id,
               t.title AS task_title,
               t.description AS task_description,
               t.due_date AS task_due_date,
               t.completed AS task_completed,
               t.created_at AS task_created_at
            FROM task_lists tl
            LEFT JOIN tasks t ON tl.id = t.task_list_id
            WHERE tl.user_id = %s
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(query, (user_id,))
            result = cursor.fetchall()
        task_lists = {}
        for row in result:
            task_list_id = row['task_list_id']
            if task_list_id not in task_lists:
                task_lists[task_list_id] = {'id': task_list_id, 'title': row['task_list_title'],
                    'description': row['task_list_description'], 'created_at': row['task_list_created_at'],
                    'tasks': []}

            if row['task_id']:
                task_lists[task_list_id]['tasks'].append(
                    {'id': row['task_id'], 'title': row['task_title'], 'description': row['task_description'],
                        'due_date': row['task_due_date'], 'completed': row['task_completed'],
                        'created_at': row['task_created_at']})
        return list(task_lists.values())


    def get_task_list(self, task_list_id):
        query = """
            SELECT id, title, description, created_at
            FROM task_lists
            WHERE id = %s
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(query, (task_list_id,))
            task_list = cursor.fetchone()
        return task_list

    def update_task_list(self, task_list_id, title, description):
        query = """
            UPDATE task_lists
            SET title = %s, description = %s
            WHERE id = %s
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(query, (title, description, task_list_id))
        self.db_conn.commit()

    def delete_task_list(self, task_list_id):
        query = """
            DELETE FROM task_lists
            WHERE id = %s
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(query, (task_list_id,))
        self.db_conn.commit()

    def create_task(self, task_list_id, title, description, due_date):
        query = """
            INSERT INTO tasks (task_list_id, title, description, due_date) 
            VALUES (%s, %s, %s, %s) 
            RETURNING id
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(query, (task_list_id, title, description, due_date))
            task_id = cursor.fetchone()[0]
        self.db_conn.commit()
        return task_id

    def get_task(self, task_id):
        query = """
            SELECT id, task_list_id, title, description, due_date, completed, created_at
            FROM tasks
            WHERE id = %s
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(query, (task_id,))
            task = cursor.fetchone()
        return task

    def update_task(self, task_id, title, description, due_date, completed):
        query = """
            UPDATE tasks
            SET title = %s, description = %s, due_date = %s, completed = %s
            WHERE id = %s
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(query, (title, description, due_date, completed, task_id))
        self.db_conn.commit()

    def delete_task(self, task_id):
        query = """
            DELETE FROM tasks
            WHERE id = %s
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(query, (task_id,))
        self.db_conn.commit()
