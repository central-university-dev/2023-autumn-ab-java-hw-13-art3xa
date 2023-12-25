from src.app.internal.tasks.repository import TaskListRepository
from src.app.internal.tasks.service import TaskListService
from src.db.di import get_db


def get_task_list_service() -> TaskListService:
    db_conn = get_db()
    task_list_repo = TaskListRepository(db_conn)
    return TaskListService(task_list_repo)
