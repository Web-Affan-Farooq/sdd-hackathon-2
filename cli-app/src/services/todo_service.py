"""
Todo service implementing business logic for task operations.
"""

from typing import List, Optional
from src.models.task import Task
from src.storage.in_memory_store import InMemoryStore


class TodoService:
    """
    Business logic layer for task operations.
    """

    def __init__(self, store: InMemoryStore):
        """
        Initialize the todo service with a storage backend.

        Args:
            store: The storage backend to use
        """
        self._store = store

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """
        Add a new task.

        Args:
            title: Task title
            description: Optional task description

        Returns:
            The created Task object
        """
        return self._store.create_task(title, description)

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get a task by ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task object if found, None otherwise
        """
        return self._store.get_task(task_id)

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            The updated Task object if successful, None if task doesn't exist
        """
        return self._store.update_task(task_id, title, description)

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: ID of the task to delete

        Returns:
            True if the task was deleted, False if it didn't exist
        """
        return self._store.delete_task(task_id)

    def list_tasks(self) -> List[Task]:
        """
        List all tasks.

        Returns:
            List of all Task objects
        """
        return self._store.list_tasks()

    def mark_complete(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as complete.

        Args:
            task_id: ID of the task to mark complete

        Returns:
            The updated Task object if successful, None if task doesn't exist
        """
        return self._store.mark_complete(task_id)

    def mark_incomplete(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as incomplete.

        Args:
            task_id: ID of the task to mark incomplete

        Returns:
            The updated Task object if successful, None if task doesn't exist
        """
        return self._store.mark_incomplete(task_id)

    def get_next_id(self) -> int:
        """
        Get the next available ID.

        Returns:
            The next available ID
        """
        return self._store.get_next_id()