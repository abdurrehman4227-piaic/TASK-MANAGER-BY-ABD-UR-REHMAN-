import json
import os
from datetime import datetime

class TodoList:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f, indent=2)
    
    def add_task(self, title, description=''):
        """Add a new task"""
        task = {
            'id': len(self.tasks) + 1,
            'title': title,
            'description': description,
            'completed': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"\n✓ Task added successfully! (ID: {task['id']})")
    
    def delete_task(self, task_id):
        """Delete a task by ID"""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                deleted = self.tasks.pop(i)
                self.save_tasks()
                print(f"\n✓ Task '{deleted['title']}' deleted successfully!")
                return
        print(f"\n✗ Task with ID {task_id} not found.")
    
    def update_task(self, task_id, title=None, description=None):
        """Update task details"""
        for task in self.tasks:
            if task['id'] == task_id:
                if title:
                    task['title'] = title
                if description is not None:
                    task['description'] = description
                self.save_tasks()
                print(f"\n✓ Task updated successfully!")
                return
        print(f"\n✗ Task with ID {task_id} not found.")
    
    def mark_complete(self, task_id):
        """Toggle task completion status"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = not task['completed']
                status = "completed" if task['completed'] else "incomplete"
                self.save_tasks()
                print(f"\n✓ Task marked as {status}!")
                return
        print(f"\n✗ Task with ID {task_id} not found.")
    
    def view_tasks(self):
        """Display all tasks"""
        if not self.tasks:
            print("\nNo tasks found. Add some tasks to get started!")
            return
        
        print("\n" + "="*70)
        print("                         YOUR TASK LIST")
        print("="*70)
        
        for task in self.tasks:
            status = "✓" if task.get('completed', False) else "○"
            print(f"\n[{status}] ID: {task.get('id', 'N/A')} | {task.get('title', 'Untitled')}")
            if task.get('description'):
                print(f"    Description: {task['description']}")
            print(f"    Created: {task.get('created_at', 'Unknown')}")
            print("-"*70)
        
        print(f"\nTotal tasks: {len(self.tasks)} | Completed: {sum(1 for t in self.tasks if t.get('completed', False))}")

def display_menu():
    """Display the main menu"""
    print("\n" + "="*70)
    print("                      TODO LIST MANAGER")
    print("="*70)
    print("\n1. Add Task")
    print("2. Delete Task")
    print("3. Update Task")
    print("4. View Task List")
    print("5. Mark as Complete/Incomplete")
    print("6. Exit")
    print("\n" + "="*70)

def main():
    todo = TodoList()
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            title = input("\nEnter task title: ").strip()
            if not title:
                print("\n✗ Task title cannot be empty!")
                continue
            description = input("Enter task description (optional): ").strip()
            todo.add_task(title, description)
        
        elif choice == '2':
            try:
                task_id = int(input("\nEnter task ID to delete: ").strip())
                todo.delete_task(task_id)
            except ValueError:
                print("\n✗ Please enter a valid task ID (number)!")
        
        elif choice == '3':
            try:
                task_id = int(input("\nEnter task ID to update: ").strip())
                title = input("Enter new title (press Enter to skip): ").strip()
                description = input("Enter new description (press Enter to skip): ").strip()
                
                if not title and not description:
                    print("\n✗ No changes provided!")
                    continue
                
                todo.update_task(
                    task_id,
                    title if title else None,
                    description if description else None
                )
            except ValueError:
                print("\n✗ Please enter a valid task ID (number)!")
        
        elif choice == '4':
            todo.view_tasks()
        
        elif choice == '5':
            try:
                task_id = int(input("\nEnter task ID to toggle completion: ").strip())
                todo.mark_complete(task_id)
            except ValueError:
                print("\n✗ Please enter a valid task ID (number)!")
        
        elif choice == '6':
            print("\nThank you for using Todo List Manager. Goodbye!")
            break
        
        else:
            print("\n✗ Invalid choice! Please select 1-6.")

if __name__ == "__main__":
    main()