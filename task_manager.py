import json
import sys
import getpass
import os
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
            return [Task(item["id"], item["title"], item["completed"]) for item in tasks]
    except FileNotFoundError:
        print("Task file not found. Creating a new one.")
        return []
    except json.JSONDecodeError:
        return []

class Task:
    def __init__(self, task_id, title, completed=False):
        self.task_id = task_id
        self.title = title
        self.completed = completed

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        return f"{self.task_id}: {self.title}, Status: {status}"

def save_tasks():
    try:
        with open("tasks.json", "w") as file:
            json.dump([{"id": task.task_id, "title": task.title, "completed": task.completed} for task in task_list], file)
    except Exception as e:
        print(f"Error saving tasks: {e}")

def add_task():
    title = input("Enter task title: ")
    task_list.append(Task(len(task_list) + 1, title))
    save_tasks()
    print("Task added successfully!")
    time.sleep(2)
    return show_main_menu()

def view_tasks():
    if not task_list:
        print("No tasks found. Please add a new task.")
        time.sleep(2)
        return show_main_menu()
    for task in task_list:
        print(task)
    action = input("Type 'exit' to return to the main menu: ")
    if action != 'exit':
        clear_screen()
        view_tasks()
    else:
        return show_main_menu()

def delete_task():
    if not task_list:
        print("No tasks to delete. Please add a task first.")
        time.sleep(2)
        return show_main_menu()

    print("Select a task to delete:")
    for task in task_list:
        print(task)
    
    task_id = int(input("Enter the task ID to delete: "))
    confirmation = input("Are you sure you want to delete this task? (yes/no): ").lower()
    
    if confirmation == "yes":
        task_list[:] = [task for task in task_list if task.task_id != task_id]
        save_tasks()
        print("Task deleted successfully.")
        time.sleep(2)
    else:
        print("Returning to the main menu.")
        time.sleep(2)

    return show_main_menu()

def mark_task_completed():
    if not task_list:
        print("No tasks to mark as completed. Please add a task first.")
        time.sleep(2)
        return show_main_menu()

    task_id = int(input("Enter the task ID to mark as completed: "))
    try:
        task = next(task for task in task_list if task.task_id == task_id)
        task.completed = True
        save_tasks()
        print("Task marked as completed!")
        time.sleep(2)
    except StopIteration:
        print("Invalid task ID. Please try again.")
        time.sleep(2)
    
    return show_main_menu()

def show_main_menu():
    clear_screen()
    print("Task Manager")
    print("1. Add a Task")
    print("2. View Tasks")
    print("3. Delete a Task")
    print("4. Mark Task as Completed")
    print("5. Exit")
    
    choice = input("Choose an option (1-5): ")

    if choice == "1":
        add_task()
    elif choice == "2":
        view_tasks()
    elif choice == "3":
        delete_task()
    elif choice == "4":
        mark_task_completed()
    elif choice == "5":
        print("Saving tasks and exiting.")
        sys.exit()
    else:
        print("Invalid choice. Please try again.")
        time.sleep(2)
        return show_main_menu()

def login():
    email_input = input("Enter your email: ")
    password_input = getpass.getpass("Enter your password: ")
    
    stored_email = "dattatri1998@gmail.com"
    stored_password = "Dattu@9764"

    if email_input == stored_email and password_input == stored_password:
        print("Login successful!")
        show_main_menu()
    else:
        print("Invalid credentials. Please try again.")
        time.sleep(2)
        clear_screen()
        login()

if __name__ == "__main__":
    task_list = load_tasks()
    login()
