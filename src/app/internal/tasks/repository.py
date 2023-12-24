class TaskListRepository:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def create_task_list(self, task_list_id, task_list):
        query = """
            INSERT INTO task_lists (id, user_id, title, description) 
            VALUES (%s, %s, %s, %s) 
            RETURNING id
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(query, (task_list_id, task_list.user_id, task_list.title, task_list.description))
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
            print(row)
            task_list_id = row[0]
            if task_list_id not in task_lists:
                task_lists[task_list_id] = {'id': task_list_id, 'title': row[1],
                    'description': row[2], 'created_at': row[3],
                    'tasks': []}

            if row[4]:
                task_lists[task_list_id]['tasks'].append(
                    {'id': row[4], 'title': row[5], 'description': row[6],
                        'due_date': row[7], 'completed': row[8],
                        'created_at': row[9]})
        return list(task_lists.values())


    def get_task_list(self, user_id, task_list_id):
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
            WHERE tl.user_id = %s AND tl.id = %s
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(query, (user_id, task_list_id))
            result = cursor.fetchall()
        task_lists = {}
        for row in result:
            task_list_id = row[0]
            if task_list_id not in task_lists:
                task_lists[task_list_id] = {'id': task_list_id, 'title': row[1],
                    'description': row[2], 'created_at': row[3],
                    'tasks': []}

            if row[4]:
                task_lists[task_list_id]['tasks'].append(
                    {'id': row[4], 'title': row[5], 'description': row[6],
                        'due_date': row[7], 'completed': row[8],
                        'created_at': row[9]})
        return list(task_lists.values())[0]


    def update_task_list(self, user_id, task_list_id, task_list):
        query = """
            UPDATE task_lists
            SET title = %s, description = %s
            WHERE user_id = %s AND id = %s
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(query, (task_list.title, task_list.description, user_id, task_list_id))
        self.db_conn.commit()

    def delete_task_list(self, user_id, task_list_id):
        query = """
            DELETE FROM task_lists
            WHERE user_id = %s AND id = %s
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(query, (user_id, task_list_id))
        self.db_conn.commit()

    def create_task(self, task_id, task):
        query = """
            INSERT INTO tasks (id, task_list_id, title, description, due_date) 
            VALUES (%s, %s, %s, %s, %s) 
            RETURNING id
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(query, (task_id, task.task_list_id, task.title, task.description, task.due_date))
            task_id = cursor.fetchone()[0]
        self.db_conn.commit()
        return task_id

    def get_task(self, task_id):
        query = """
            SELECT id, title, description, due_date, completed, created_at
            FROM tasks
            WHERE id = %s
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(query, (task_id,))
            task = cursor.fetchone()
        return task

    def get_tasks(self, task_list_id):
        query = """
            SELECT id, title, description, due_date, completed, created_at
            FROM tasks
            WHERE task_list_id = %s
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(query, (task_list_id,))
            tasks = cursor.fetchall()
        return tasks

    def update_task(self, task_id, task):
        query = """
            UPDATE tasks
            SET title = %s, description = %s, due_date = %s, completed = %s
            WHERE id = %s
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(query, (task.title, task.description, task.due_date, task.completed, task_id))
        self.db_conn.commit()

    def delete_task(self, task_id):
        query = """
            DELETE FROM tasks
            WHERE id = %s
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(query, (task_id,))
        self.db_conn.commit()
