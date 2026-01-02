import sys
sys.path.insert(0, '.')

from src.models.task import Task
from src.storage.in_memory_store import InMemoryStore
from src.services.todo_service import TodoService

def test_basic_functionality():
    """Test the basic functionality of the todo application."""
    print("Testing basic functionality...")

    # Test basic functionality
    store = InMemoryStore()
    service = TodoService(store)

    # Test adding a task
    task = service.add_task('Test task', 'Test description')
    print(f'✓ Added task: ID={task.id}, Title={task.title}, Completed={task.completed}')

    # Test listing tasks
    tasks = service.list_tasks()
    print(f'✓ Number of tasks: {len(tasks)}')

    # Test updating a task
    updated_task = service.update_task(task.id, 'Updated title')
    print(f'✓ Updated task: {updated_task.title if updated_task else None}')

    # Test marking as complete
    completed_task = service.mark_complete(task.id)
    print(f'✓ Marked as complete: {completed_task.completed if completed_task else None}')

    # Test marking as incomplete
    incomplete_task = service.mark_incomplete(task.id)
    print(f'✓ Marked as incomplete: {incomplete_task.completed if incomplete_task else None}')

    # Test deleting a task
    success = service.delete_task(task.id)
    print(f'✓ Deleted task: {success}')

    # Verify task is deleted
    tasks = service.list_tasks()
    print(f'✓ Number of tasks after deletion: {len(tasks)}')

    print('✓ All basic functionality tests passed!')

if __name__ == "__main__":
    test_basic_functionality()