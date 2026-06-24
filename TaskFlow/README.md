# ✦ TaskFlow - To-Do Manager

TaskFlow is a modern desktop-based To-Do List application built using **Python Tkinter**. It helps users organize tasks efficiently with categories, deadlines, search functionality, task completion tracking, and persistent storage.

## 📌 Features

### ✅ Task Management

* Add new tasks with title, description, category, and deadline.
* Edit existing tasks.
* Mark tasks as completed.
* Delete tasks with confirmation prompts.

### 📂 Categories

Tasks can be organized into:

* Work
* Personal
* Urgent
* Other

Users can filter tasks by category for better organization.

### 🔍 Search Functionality

* Instantly search tasks by title or description.
* Dynamic filtering as you type.

### 📅 Deadline Tracking

* Optional deadlines for tasks.
* Highlights:

  * Overdue tasks
  * Tasks due today
  * Tasks due within the next few days

### 📊 Progress Tracking

* Displays completion statistics.
* Shows completed vs total tasks.

### 💾 Persistent Storage

* Tasks are automatically saved to a local JSON file (`tasks.json`).
* Data remains available between application sessions.

### 🎨 Modern User Interface

* Dark-themed design.
* Color-coded task categories.
* Interactive buttons and task cards.
* Scrollable task list.

---

## 🛠 Technologies Used

* Python 3
* Tkinter (GUI Framework)
* JSON (Data Storage)
* ttk Widgets

---

## 📁 Project Structure

```text
TaskFlow/
│
├── taskflow.py        # Main application file
├── tasks.json         # Automatically generated task database
└── README.md          # Project documentation
```

---

## 🚀 Installation & Execution

### Prerequisites

Make sure Python 3 is installed:

```bash
python --version
```

### Run the Application

1. Clone or download the project.

2. Navigate to the project folder:

```bash
cd TaskFlow
```

3. Run the application:

```bash
python taskflow.py
```

---

## 📖 How to Use

### Adding a Task

1. Click **"+ New Task"**.
2. Enter:

   * Title
   * Description (optional)
   * Category
   * Deadline (optional)
3. Click **Add Task**.

### Editing a Task

1. Click the **Edit** button.
2. Modify the task details.
3. Save changes.

### Completing a Task

Click the **Done** button to mark a task as completed.

### Deleting a Task

Click the **Delete** button and confirm the action.

### Searching Tasks

Use the search bar to find tasks by title or description.

---

## 🎯 Future Enhancements

* Task priority levels
* Notifications and reminders
* Calendar integration
* Export tasks to CSV/PDF
* Light/Dark theme switching
* Drag-and-drop task organization
* Task statistics dashboard

---

## 👨‍💻 Author

Developed as a Python GUI project using Tkinter to demonstrate:

* Object-Oriented Programming
* File Handling
* GUI Development
* Data Persistence
* User Experience Design

---

## 📄 License

This project is open-source and available for educational and personal use.
