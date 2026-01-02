"""
Task model representing a todo item with ID, title, description, and completion status.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """
    Represents a todo task with required fields and validation.
    """
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    def __post_init__(self):
        """
        Validate the task after initialization.
        """
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("Task ID must be a positive integer")
        if not isinstance(self.completed, bool):
            raise ValueError("Task completion status must be a boolean")

    def mark_complete(self):
        """Mark the task as complete."""
        self.completed = True

    def mark_incomplete(self):
        """Mark the task as incomplete."""
        self.completed = False

    def update(self, title: Optional[str] = None, description: Optional[str] = None):
        """Update task title and/or description."""
        if title is not None:
            if not title.strip():
                raise ValueError("Task title cannot be empty")
            self.title = title
        if description is not None:
            self.description = description