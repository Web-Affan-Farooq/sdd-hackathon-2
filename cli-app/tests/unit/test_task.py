"""
Unit tests for the Task model.
"""

import pytest
from src.models.task import Task


class TestTask:
    """
    Unit tests for the Task model.
    """

    def test_task_creation_with_valid_data(self):
        """Test creating a task with valid data."""
        task = Task(id=1, title="Test Task", description="Test Description", completed=False)

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False

    def test_task_creation_with_minimal_data(self):
        """Test creating a task with minimal required data."""
        task = Task(id=1, title="Test Task")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description is None
        assert task.completed is False

    def test_task_creation_with_completed_true(self):
        """Test creating a task with completed status."""
        task = Task(id=1, title="Test Task", completed=True)

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.completed is True

    def test_task_title_cannot_be_empty(self):
        """Test that creating a task with empty title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(id=1, title="")

    def test_task_title_cannot_be_whitespace_only(self):
        """Test that creating a task with whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(id=1, title="   ")

    def test_task_id_must_be_positive_integer(self):
        """Test that creating a task with non-positive ID raises ValueError."""
        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            Task(id=0, title="Test Task")

        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            Task(id=-1, title="Test Task")

    def test_task_completion_must_be_boolean(self):
        """Test that creating a task with non-boolean completion status raises ValueError."""
        with pytest.raises(ValueError, match="Task completion status must be a boolean"):
            Task(id=1, title="Test Task", completed="true")

    def test_mark_complete(self):
        """Test marking a task as complete."""
        task = Task(id=1, title="Test Task", completed=False)
        task.mark_complete()

        assert task.completed is True

    def test_mark_incomplete(self):
        """Test marking a task as incomplete."""
        task = Task(id=1, title="Test Task", completed=True)
        task.mark_incomplete()

        assert task.completed is False

    def test_update_task_title(self):
        """Test updating task title."""
        task = Task(id=1, title="Old Title")
        task.update(title="New Title")

        assert task.title == "New Title"

    def test_update_task_description(self):
        """Test updating task description."""
        task = Task(id=1, title="Test Task", description="Old Description")
        task.update(description="New Description")

        assert task.description == "New Description"

    def test_update_task_title_and_description(self):
        """Test updating both title and description."""
        task = Task(id=1, title="Old Title", description="Old Description")
        task.update(title="New Title", description="New Description")

        assert task.title == "New Title"
        assert task.description == "New Description"

    def test_update_task_title_cannot_be_empty(self):
        """Test that updating task title to empty raises ValueError."""
        task = Task(id=1, title="Old Title")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            task.update(title="")

    def test_update_task_title_cannot_be_whitespace_only(self):
        """Test that updating task title to whitespace-only raises ValueError."""
        task = Task(id=1, title="Old Title")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            task.update(title="   ")