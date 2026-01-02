"""
In-memory storage for tasks with auto-incrementing IDs.
"""

from typing import Dict, List, Optional
from src.models.task import Task


class InMemoryStore:
    """
    In-memory storage for tasks with deterministic auto-incrementing IDs.
    """

    def __init__(self):
        """
        Initialize the in-memory store with an empty task dictionary and ID counter.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def create_task(self, title: str, description: Optional[str] = None) -> Task:
        """
        Create a new task with auto-assigned ID.

        Args:
            title: Task title
            description: Optional task description

        Returns:
            The created Task object with assigned ID
        """
        task_id = self._next_id
        self._next_id += 1
        task = Task(id=task_id, title=title, description=description, completed=False)
        self._tasks[task_id] = task
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task object if found, None otherwise
        """
        return self._tasks.get(task_id)

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
        task = self.get_task(task_id)
        if task is None:
            return None

        task.update(title=title, description=description)
        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: ID of the task to delete

        Returns:
            True if the task was deleted, False if it didn't exist
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def list_tasks(self) -> List[Task]:
        """
        Return all tasks.

        Returns:
            List of all Task objects
        """
        return list(self._tasks.values())

    def mark_complete(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as complete.

        Args:
            task_id: ID of the task to mark complete

        Returns:
            The updated Task object if successful, None if task doesn't exist
        """
        task = self.get_task(task_id)
        if task is None:
            return None

        task.mark_complete()
        return task

    def mark_incomplete(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as incomplete.

        Args:
            task_id: ID of the task to mark incomplete

        Returns:
            The updated Task object if successful, None if task doesn't exist
        """
        task = self.get_task(task_id)
        if task is None:
            return None

        task.mark_incomplete()
        return task

    def get_next_id(self) -> int:
        """
        Get the next available ID (for internal use).

        Returns:
            The next available ID
        """
        return self._next_id - 1 if self._next_id > 1 else 0  # Return the last assigned ID