"""
Integration tests for the TodoService update and delete operations.
"""

from src.services.todo_service import TodoService
from src.storage.in_memory_store import InMemoryStore


class TestTodoServiceUpdateDelete:
    """
    Integration tests for the TodoService update and delete operations.
    """

    def setup_method(self):
        """Set up a fresh service for each test."""
        self.store = InMemoryStore()
        self.service = TodoService(self.store)

    def test_update_task_title(self):
        """Test updating a task's title."""
        task = self.service.add_task("Old Title", "Description")
        updated_task = self.service.update_task(task.id, "New Title")

        assert updated_task is not None
        assert updated_task.title == "New Title"
        assert updated_task.description == "Description"

    def test_update_task_description(self):
        """Test updating a task's description."""
        task = self.service.add_task("Title", "Old Description")
        updated_task = self.service.update_task(task.id, description="New Description")

        assert updated_task is not None
        assert updated_task.title == "Title"
        assert updated_task.description == "New Description"

    def test_update_task_title_and_description(self):
        """Test updating both title and description."""
        task = self.service.add_task("Old Title", "Old Description")
        updated_task = self.service.update_task(task.id, "New Title", "New Description")

        assert updated_task is not None
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"

    def test_update_nonexistent_task_returns_none(self):
        """Test that updating a non-existent task returns None."""
        result = self.service.update_task(999, "New Title")

        assert result is None

    def test_update_task_with_empty_title_raises_error(self):
        """Test that updating a task with empty title raises an error."""
        task = self.service.add_task("Old Title")

        try:
            self.service.update_task(task.id, "")
            assert False, "Expected ValueError was not raised"
        except ValueError:
            pass  # Expected

    def test_delete_task_removes_it_from_store(self):
        """Test that deleting a task removes it from the store."""
        task = self.service.add_task("Title", "Description")
        success = self.service.delete_task(task.id)

        assert success is True
        remaining_tasks = self.service.list_tasks()
        assert len(remaining_tasks) == 0

    def test_delete_nonexistent_task_returns_false(self):
        """Test that deleting a non-existent task returns False."""
        success = self.service.delete_task(999)

        assert success is False

    def test_delete_task_does_not_affect_other_tasks(self):
        """Test that deleting one task doesn't affect others."""
        task1 = self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")
        task3 = self.service.add_task("Task 3")

        success = self.service.delete_task(task2.id)

        assert success is True
        remaining_tasks = self.service.list_tasks()
        assert len(remaining_tasks) == 2
        remaining_ids = [t.id for t in remaining_tasks]
        assert task1.id in remaining_ids
        assert task3.id in remaining_ids
        assert task2.id not in remaining_ids

    def test_update_and_delete_sequence(self):
        """Test a sequence of update and delete operations."""
        task1 = self.service.add_task("Task 1", "Description 1")
        task2 = self.service.add_task("Task 2", "Description 2")

        # Update first task
        updated_task1 = self.service.update_task(task1.id, "Updated Task 1", "Updated Description 1")
        assert updated_task1 is not None
        assert updated_task1.title == "Updated Task 1"

        # Delete second task
        success = self.service.delete_task(task2.id)
        assert success is True

        # Verify first task was updated and second was deleted
        remaining_tasks = self.service.list_tasks()
        assert len(remaining_tasks) == 1
        assert remaining_tasks[0].title == "Updated Task 1"
        assert remaining_tasks[0].description == "Updated Description 1"