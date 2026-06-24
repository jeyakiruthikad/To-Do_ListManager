# ✦ TaskFlow - To-Do List Manager

---

## 📌 Overview

TaskFlow is designed to improve productivity by providing a clean and intuitive interface for managing tasks. Users can create tasks, assign categories, set deadlines, track completion status, and store task data permanently using JSON files.

The application follows an object-oriented design and demonstrates GUI development using Python's Tkinter library.

---

## ✨ Features

### 📝 Task Management

* Add new tasks
* Edit existing tasks
* Delete tasks
* Mark tasks as completed

### 📂 Category-Based Organization

Tasks can be organized into:

* Work
* Personal
* Urgent
* Other

### 📅 Deadline Tracking

* Set deadlines for tasks
* Highlight overdue tasks
* Indicate tasks due today
* Show upcoming deadlines

### 🔍 Search Functionality

* Search tasks by title
* Search tasks by description
* Real-time filtering while typing

### 📊 Progress Monitoring

* Displays total tasks
* Displays completed tasks
* Tracks productivity progress

### 💾 Data Persistence

* Tasks are automatically saved in a JSON file
* Data remains available between application sessions

### 🎨 Modern User Interface

* Dark-themed design
* Interactive buttons with hover effects
* Scrollable task dashboard
* Category color indicators

---

## 🛠️ Technologies Used

| Technology | Purpose                   |
| ---------- | ------------------------- |
| Python     | Core Programming Language |
| Tkinter    | GUI Development           |
| JSON       | Data Storage              |
| OOP        | Application Structure     |

---

## 📂 Project Structure

```text
TaskFlow/
│
├── todo.py      # Main application source code
├── tasks.json       # Stores all task information
└── README.md        # Project documentation
```

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/jeyakiruthikad/To-Do_ListManager.git
cd To-Do_ListManager
```

### Step 2: Verify Python Installation

```bash
python --version
```

Python 3.8 or above is recommended.

### Step 3: Run the Application

```bash
python todo.py
```

---

## 📖 Usage Guide

### Adding a Task

1. Click **"+ New Task"**
2. Enter:

   * Task Title
   * Description (Optional)
   * Category
   * Deadline (Optional)
3. Click **Add Task**

### Editing a Task

1. Select **Edit**
2. Modify task details
3. Save changes

### Completing a Task

1. Click **Done**
2. Task will be marked as completed

### Deleting a Task

1. Click **Delete**
2. Confirm deletion

### Searching Tasks

Use the search bar to instantly find tasks by title or description.

### Filtering Tasks

Choose a category from the sidebar to display only related tasks.

---

## 🔮 Future Enhancements

* Priority Levels
* Calendar View
* Task Reminders & Notifications
* Export Tasks to PDF
* Cloud Synchronization
* User Authentication
* Light/Dark Theme Toggle
* Drag-and-Drop Task Sorting

---

## 👨‍💻 Author

Developed as a Python GUI project to demonstrate task management, persistent storage, and modern desktop application development using Tkinter.

---

## 📄 License

This project is open-source and intended for educational and personal use.
