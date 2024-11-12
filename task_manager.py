import json
import sys
import getpass
import os
import time

# Function to clear the terminal screen based on OS
def clear_screen():
    # If the OS is Windows ('nt'), use 'cls', else use 'clear' for Unix-like systems
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to load tasks from a JSON file
def load_tasks():
    try:
        # Attempt to open and load tasks from the tasks.json file
        with open("tasks.json", "r") as file:
            tasks = json.load(file)  # Load the data into a list of dictionaries
            # Convert each dictionary into a Task object
            return [Task(item["id"], item["title"], item["completed"]) for item in tasks]
    except FileNotFoundError:
        # If the file doesn't exist, print a message and return an empty list
        print("Task file not found. Creating a new one.")
        return []
    except json.JSONDecodeError:
        # If there's an issue parsing the JSON, return an empty list
        return []

# Task class to represent individual tasks with an ID, title, and completion status
class Task:
    def __init__(self, task_id, title, completed=False):
        # Initialize the task with an ID, title, and completed status
        self.task_id = task_id
        self.title = title
        self.completed = completed

    def __str__(self):
        # Return a string representation of the task with its ID, title, and status
        status = "Completed" if self.completed else "Pending"
        return f"{self.task_id}: {self.title}, Status: {status}"

# Function to save the current list of tasks to tasks.json
def save_tasks():
    try:
        # Open the tasks.json file in write mode
        with open("tasks.json", "w") as file:
            # Save the list of tasks as a JSON array of dictionaries
            json.dump([{"id": task.task_id, "title": task.title, "completed": task.completed} for task in task_list], file)
    except Exception as e:
        # If an error occurs during saving, print the error message
        print(f"Error saving tasks: {e}")

# Function to add a new task
def add_task():
    # Prompt the user for the task title
    title = input("Enter task title: ")
    # Create a new task object with the next available task ID and the entered title
    task_list.append(Task(len(task_list) + 1, title))
    # Save the updated task list to the file
    save_tasks()
    print("Task added successfully!")
    # Pause for 2 seconds before returning to the main menu
    time.sleep(2)
    return show_main_menu()

# Function to view all tasks
def view_tasks():
    if not task_list:
        # If there are no tasks, inform the user and return to the main menu
        print("No tasks found. Please add a new task.")
        time.sleep(2)
        return show_main_menu()
    
    # Print each task in the task list
    for task in task_list:
        print(task)
    
    # Prompt the user to exit or continue
    action = input("Type 'exit' to return to the main menu: ")
    if action != 'exit':
        # If the user doesn't type 'exit', clear the screen and show the task list again
        clear_screen()
        view_tasks()
    else:
        # If the user types 'exit', return to the main menu
        return show_main_menu()

# Function to delete a task by its ID
def delete_task():
    if not task_list:
        # If there are no tasks to delete, inform the user and return to the main menu
        print("No tasks to delete. Please add a task first.")
        time.sleep(2)
        return show_main_menu()

    print("Select a task to delete:")
    # Display the list of tasks with their IDs
    for task in task_list:
        print(task)
    
    # Prompt the user for the task ID to delete
    task_id = int(input("Enter the task ID to delete: "))
    confirmation = input("Are you sure you want to delete this task? (yes/no): ").lower()
    
    if confirmation == "yes":
        # Remove the task with the given ID from the list
        task_list[:] = [task for task in task_list if task.task_id != task_id]
        # Save the updated task list to the file
        save_tasks()
        print("Task deleted successfully.")
        time.sleep(2)
    else:
        # If the user doesn't confirm, print a message and return to the main menu
        print("Returning to the main menu.")
        time.sleep(2)

    return show_main_menu()

# Function to mark a task as completed
def mark_task_completed():
    if not task_list:
        # If there are no tasks, inform the user and return to the main menu
        print("No tasks to mark as completed. Please add a task first.")
        time.sleep(2)
        return show_main_menu()

    # Prompt the user for the task ID to mark as completed
    task_id = int(input("Enter the task ID to mark as completed: "))
    try:
        # Find the task with the given ID
        task = next(task for task in task_list if task.task_id == task_id)
        # Mark the task as completed
        task.completed = True
        # Save the updated task list
        save_tasks()
        print("Task marked as completed!")
        time.sleep(2)
    except StopIteration:
        # If the task ID is not valid, inform the user
        print("Invalid task ID. Please try again.")
        time.sleep(2)
    
    return show_main_menu()

# Function to display the main menu with options
def show_main_menu():
    clear_screen()
    print("Task Manager")
    print("1. Add a Task")
    print("2. View Tasks")
    print("3. Delete a Task")
    print("4. Mark Task as Completed")
    print("5. Exit")
    
    # Prompt the user to choose an option
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
        # Print a message and exit the program
        print("Saving tasks and exiting.")
        sys.exit()
    else:
        # If the user chooses an invalid option, show an error message and prompt again
        print("Invalid choice. Please try again.")
        time.sleep(2)
        return show_main_menu()

# Function to handle user login
def login():
    # Prompt the user for their email and password
    email_input = input("Enter your email: ")
    password_input = getpass.getpass("Enter your password: ")
    
    # Stored credentials (hardcoded for simplicity)
    stored_email = "dattatri1998@gmail.com"
    stored_password = "Dattu@9764"

    if email_input == stored_email and password_input == stored_password:
        # If the credentials match, print a success message and show the main menu
        print("Login successful!")
        show_main_menu()
    else:
        # If the credentials don't match, print an error message and prompt again
        print("Invalid credentials. Please try again.")
        time.sleep(2)
        clear_screen()
        login()

# Main entry point of the program
if __name__ == "__main__":
    # Load the task list from the tasks.json file
    task_list = load_tasks()
    # Start the login process
    login()
