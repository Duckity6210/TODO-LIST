todos-api
# Todo List API

A simple Todo List API built using Python and a backend framework (e.g., Flask). This API allows users to manage their tasks, including creating, reading, updating, and deleting (CRUD) operations.

## Features

- **Create** new tasks.
- **Read** a list of tasks or individual task details.
- **Update** existing tasks.
- **Delete** tasks.
- **Mark tasks** as complete/incomplete.

## Getting Started

### Prerequisites

- Python 3
- [Backend framework] i.e Flask
- virtual environment (venv)
- gunicorn for production
- pip (Python package installer)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Duckity6210/todo-api.git
   cd todo-api

 I.P Adress where API is running
  http://127.0.0.1:5000
GET ALL TASKS

curl -X GET http://127.0.0.1:5000/tasks

GET TASK BY ID

curl -X GET http://127.0.0.1:5000/tasks/{task_id}

POST NEW TASK

curl -X POST http://127.0.0.1:5000/tasks -H "Content-Type: application/json" -d '{"title": "{title}"}'

DELETE TASK

curl -X DELETE http://127.0.0.1:5000/tasks/{task_id}

PUT TASK

curl -X PUT http://127.0.0.1:5000/tasks/{1} -H "Content-Type: application/json" -d '{"title": "Go To Gym", "done": true}' 
