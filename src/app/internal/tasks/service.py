from src.app.internal.tasks.dto import (
    TaskCreateDTO,
    TaskDTO,
    TaskListCreateDTO,
    TaskListDTO,
    TaskListUpdateDTO,
    TaskUpdateDTO,
)
from src.app.internal.tasks.repository import TaskListRepository


class TaskListService:
    def __init__(self, task_list_repo: TaskListRepository):
        self.task_list_repo = task_list_repo

    def get_task_lists(self, user_id: str) -> list[TaskListDTO]:
        task_lists = self.task_list_repo.get_task_lists(user_id)
        task_lists_dto = []
        for task_list in task_lists:
            tasks_dto = []
            for task in task_list['tasks']:
                task_dto = TaskDTO(
                    id=task['id'],
                    title=task['title'],
                    description=task['description'],
                    due_date=task['due_date'].isoformat(),
                    completed=task['completed'],
                    created_at=task['created_at'].isoformat(),
                )
                tasks_dto.append(task_dto)
            task_list_dto = TaskListDTO(
                id=task_list['id'],
                title=task_list['title'],
                description=task_list['description'],
                created_at=task_list['created_at'].isoformat(),
                tasks=tasks_dto,
            )
            task_lists_dto.append(task_list_dto.model_dump())
        return task_lists_dto

    def get_task_list(self, user_id, task_list_id) -> TaskListDTO:
        task_list = self.task_list_repo.get_task_list(user_id, task_list_id)
        tasks_dto = []
        for task in task_list['tasks']:
            task_dto = TaskDTO(
                id=task['id'],
                title=task['title'],
                description=task['description'],
                due_date=task['due_date'].isoformat(),
                completed=task['completed'],
                created_at=task['created_at'].isoformat(),
            )
            tasks_dto.append(task_dto)
        task_list_dto = TaskListDTO(
            id=task_list['id'],
            title=task_list['title'],
            description=task_list['description'],
            created_at=task_list['created_at'].isoformat(),
            tasks=tasks_dto,
        )
        return task_list_dto.model_dump()

    def create_task_list(self, task_list_id: str, task_list: TaskListCreateDTO) -> str:
        task_list_id = self.task_list_repo.create_task_list(task_list_id, task_list)
        return task_list_id

    def update_task_list(self, user_id: str, task_list_id: str, task_list: TaskListUpdateDTO) -> None:
        self.task_list_repo.update_task_list(user_id, task_list_id, task_list)

    def delete_task_list(self, user_id: str, task_list_id: str) -> None:
        self.task_list_repo.delete_task_list(user_id, task_list_id)

    def get_tasks(self, task_list_id: str) -> list[TaskDTO]:
        tasks = self.task_list_repo.get_tasks(task_list_id)
        tasks_dto = []
        for task in tasks:
            task_dto = TaskDTO(
                id=task[0],
                title=task[1],
                description=task[2],
                due_date=task[3].isoformat(),
                completed=task[4],
                created_at=task[5].isoformat(),
            )
            tasks_dto.append(task_dto.model_dump())
        return tasks_dto

    def get_task(self, task_id: str) -> TaskDTO:
        task = self.task_list_repo.get_task(task_id)
        task_dto = TaskDTO(
            id=task[0],
            title=task[1],
            description=task[2],
            due_date=task[3].isoformat(),
            completed=task[4],
            created_at=task[5].isoformat(),
        )
        return task_dto.model_dump()

    def create_task(self, task_id: str, task: TaskCreateDTO) -> str:
        task_id = self.task_list_repo.create_task(task_id, task)
        return task_id

    def update_task(self, task_id: str, task: TaskUpdateDTO) -> None:
        self.task_list_repo.update_task(task_id, task)

    def delete_task(self, task_id: str) -> None:
        self.task_list_repo.delete_task(task_id)
