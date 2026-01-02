"""
Integration tests for the TodoService add and list operations.
"""

from src.services.todo_service import TodoService
from src.storage.in_memory_store import InMemoryStore


class TestTodoService:
    """
    Integration tests for the TodoService.
    """

    def setup_method(self):
        """Set up a fresh service for each test."""
        self.store = InMemoryStore()
        self.service = TodoService(self.store)

    def test_add_task_creates_task(self):
        """Test that adding a task creates it in the store."""
        task = self.service.add_task("Test Title", "Test Description")

        assert task.title == "Test Title"
        assert task.description == "Test Description"
        assert task.completed is False
        assert task.id == 1

    def test_add_multiple_tasks_have_sequential_ids(self):
        """Test that multiple tasks get sequential IDs."""
        task1 = self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")
        task3 = self.service.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_list_tasks_returns_all_tasks(self):
        """Test that listing tasks returns all added tasks."""
        task1 = self.service.add_task("Task 1", "Description 1")
        task2 = self.service.add_task("Task 2", "Description 2")
        task3 = self.service.add_task("Task 3")

        tasks = self.service.list_tasks()

        assert len(tasks) == 3
        assert tasks[0].id == 1
        assert tasks[0].title == "Task 1"
        assert tasks[0].description == "Description 1"
        assert tasks[1].id == 2
        assert tasks[1].title == "Task 2"
        assert tasks[1].description == "Description 2"
        assert tasks[2].id == 3
        assert tasks[2].title == "Task 3"
        assert tasks[2].description is None

    def test_add_task_with_empty_title_raises_error(self):
        """Test that adding a task with empty title raises an error."""
        try:
            self.service.add_task("")
            assert False, "Expected ValueError was not raised"
        except ValueError:
            pass  # Expected

    def test_list_tasks_returns_empty_list_when_no_tasks(self):
        """Test that listing tasks returns an empty list when no tasks exist."""
        tasks = self.service.list_tasks()

        assert len(tasks) == 0

    def test_add_task_assigns_correct_id(self):
        """Test that tasks get correct IDs even after some are deleted."""
        task1 = self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")
        self.service.delete_task(1)  # Delete first task
        task3 = self.service.add_task("Task 3")

        # Task 3 should have ID 3, not 2, because we keep sequential IDs
        assert task3.id == 3

    def test_get_task_by_id(self):
        """Test retrieving a specific task by ID."""
        task = self.service.add_task("Test Task", "Test Description")
        retrieved_task = self.service.get_task(task.id)

        assert retrieved_task is not None
        assert retrieved_task.id == task.id
        assert retrieved_task.title == task.title
        assert retrieved_task.description == task.description
        assert retrieved_task.completed == task.completed

    def test_get_nonexistent_task_returns_none(self):
        """Test that getting a non-existent task returns None."""
        result = self.service.get_task(999)

        assert result is None

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

    def test_mark_task_complete(self):
        """Test marking a task as complete."""
        task = self.service.add_task("Test Task", "Description")
        assert task.completed is False

        completed_task = self.service.mark_complete(task.id)
        assert completed_task is not None
        assert completed_task.completed is True

    def test_mark_task_incomplete(self):
        """Test marking a task as incomplete."""
        task = self.service.add_task("Test Task", "Description")
        task = self.service.mark_complete(task.id)  # First mark as complete
        assert task.completed is True

        incomplete_task = self.service.mark_incomplete(task.id)
        assert incomplete_task is not None
        assert incomplete_task.completed is False

    def test_mark_nonexistent_task_returns_none(self):
        """Test that marking a non-existent task returns None."""
        result = self.service.mark_complete(999)
        assert result is None

        result = self.service.mark_incomplete(999)
        assert result is None

    def test_mark_complete_and_incomplete_sequence(self):
        """Test a sequence of marking tasks complete and incomplete."""
        task1 = self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")

        # Mark first task as complete
        completed_task1 = self.service.mark_complete(task1.id)
        assert completed_task1.completed is True

        # Mark second task as complete
        completed_task2 = self.service.mark_complete(task2.id)
        assert completed_task2.completed is True

        # Mark first task as incomplete
        incomplete_task1 = self.service.mark_incomplete(task1.id)
        assert incomplete_task1.completed is False

        # Verify current states
        all_tasks = self.service.list_tasks()
        task_dict = {t.id: t for t in all_tasks}
        assert task_dict[task1.id].completed is False  # Task 1 is incomplete
        assert task_dict[task2.id].completed is True   # Task 2 is complete