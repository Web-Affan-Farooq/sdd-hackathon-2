"""
CLI interface for the todo application using questionary for interactive prompts.
"""

import argparse
import sys
from typing import Optional
import questionary
from src.services.todo_service import TodoService
from src.storage.in_memory_store import InMemoryStore


class TodoCLI:
    """
    Command-line interface for the todo application.
    """

    def __init__(self):
        """
        Initialize the CLI with a todo service.
        """
        self.store = InMemoryStore()
        self.service = TodoService(self.store)

    def add_task(self, title: Optional[str] = None, description: Optional[str] = None):
        """
        Add a new task with optional title and description.
        If not provided, prompt interactively.
        """
        if not title:
            title = questionary.text("Enter task title:").ask()
            if not title:
                print("Error: Task title is required.")
                return

        if description is None:
            description = questionary.text("Enter task description (optional):").ask()
            if description == "":
                description = None

        try:
            task = self.service.add_task(title, description)
            print(f"✓ Task added successfully with ID {task.id}: {task.title}")
        except ValueError as e:
            print(f"Error adding task: {e}")

    def list_tasks(self):
        """
        List all tasks with their IDs, titles, descriptions, and completion status.
        """
        tasks = self.service.list_tasks()
        if not tasks:
            print("No tasks found.")
            return

        print("\nYour Tasks:")
        print("=" * 80)
        for task in tasks:
            status = "✓" if task.completed else "○"
            desc = f"\n    Description: {task.description}" if task.description else ""
            print(f"{status} [{task.id:2d}] {task.title}{desc}")
        print("=" * 80)
        print(f"Total: {len(tasks)} task{'s' if len(tasks) != 1 else ''}")

    def update_task(self, task_id: Optional[int] = None, title: Optional[str] = None, description: Optional[str] = None):
        """
        Update an existing task.
        """
        if not task_id:
            task_id = self._get_task_id_prompt("update")
            if task_id is None:
                return

        # Get current task to show current values
        current_task = self.service.get_task(task_id)
        if not current_task:
            print(f"Error: Task with ID {task_id} not found.")
            return

        # If title or description not provided, prompt interactively
        if title is None:
            title_input = questionary.text(
                f"Enter new title (current: '{current_task.title}', press Enter to keep current):"
            ).ask()
            if title_input == "":
                title = current_task.title
            else:
                title = title_input if title_input else None

        if description is None:
            desc_input = questionary.text(
                f"Enter new description (current: '{current_task.description or 'None'}', press Enter to keep current):"
            ).ask()
            if desc_input == "":
                description = current_task.description
            else:
                description = desc_input if desc_input != "None" else None

        try:
            updated_task = self.service.update_task(task_id, title, description)
            if updated_task:
                print(f"Task {task_id} updated successfully.")
            else:
                print(f"Error: Failed to update task {task_id}. Task may not exist.")
        except ValueError as e:
            print(f"Error updating task: {e}")

    def delete_task(self, task_id: Optional[int] = None):
        """
        Delete a task by ID.
        """
        if not task_id:
            task_id = self._get_task_id_prompt("delete")
            if task_id is None:
                return

        success = self.service.delete_task(task_id)
        if success:
            print(f"Task {task_id} deleted successfully.")
        else:
            print(f"Error: Task with ID {task_id} not found.")

    def complete_task(self, task_id: Optional[int] = None):
        """
        Mark a task as complete.
        """
        if not task_id:
            task_id = self._get_task_id_prompt("mark complete")
            if task_id is None:
                return

        task = self.service.mark_complete(task_id)
        if task:
            print(f"Task {task_id} marked as complete.")
        else:
            print(f"Error: Task with ID {task_id} not found.")

    def incomplete_task(self, task_id: Optional[int] = None):
        """
        Mark a task as incomplete.
        """
        if not task_id:
            task_id = self._get_task_id_prompt("mark incomplete")
            if task_id is None:
                return

        task = self.service.mark_incomplete(task_id)
        if task:
            print(f"Task {task_id} marked as incomplete.")
        else:
            print(f"Error: Task with ID {task_id} not found.")

    def _get_task_id_prompt(self, action: str) -> Optional[int]:
        """
        Prompt user for a task ID with validation.
        """
        tasks = self.service.list_tasks()
        if not tasks:
            print("No tasks available.")
            return None

        task_choices = [f"[{task.id}] {task.title}" for task in tasks]
        selected = questionary.select(
            f"Select task to {action}:",
            choices=task_choices
        ).ask()

        if not selected:
            return None

        # Extract ID from the selection "[ID] title"
        task_id = int(selected.split(']')[0].split('[')[1])
        return task_id


def main():
    """
    Main entry point for the CLI application.
    """
    cli = TodoCLI()

    parser = argparse.ArgumentParser(description="In-Memory Todo CLI Application")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", nargs="?", help="Task title")
    add_parser.add_argument("description", nargs="?", help="Task description")

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", type=int, nargs="?", help="Task ID")
    update_parser.add_argument("title", nargs="?", help="New task title")
    update_parser.add_argument("description", nargs="?", help="New task description")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, nargs="?", help="Task ID")

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark task as complete")
    complete_parser.add_argument("id", type=int, nargs="?", help="Task ID")

    # Incomplete command
    incomplete_parser = subparsers.add_parser("incomplete", help="Mark task as incomplete")
    incomplete_parser.add_argument("id", type=int, nargs="?", help="Task ID")

    args = parser.parse_args()

    try:
        if not args.command:
            # No command provided, show help
            parser.print_help()
            return

        if args.command == "add":
            cli.add_task(args.title, args.description)
        elif args.command == "list":
            cli.list_tasks()
        elif args.command == "update":
            cli.update_task(args.id, args.title, args.description)
        elif args.command == "delete":
            cli.delete_task(args.id)
        elif args.command == "complete":
            cli.complete_task(args.id)
        elif args.command == "incomplete":
            cli.incomplete_task(args.id)
        else:
            parser.print_help()
    except ValueError as e:
        print(f"Value Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()