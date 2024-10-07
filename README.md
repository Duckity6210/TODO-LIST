
Navigation Menu

Code
Issues
Pull requests
BreadcrumbsTODO-LIST
/todos-api/
Directory actionsMore options
Latest commit
Duckity6210
Duckity6210
last week
History
BreadcrumbsTODO-LIST
/todos-api/
Folders and files
Name	Last commit date
parent directory
..
__pycache__
last week
instance
last week
venv
last week
Procfile
last week
README.md
last week
app.py
last week
requirements.txt
last week
README.md
todos-api

Todo List API
A simple Todo List API built using Python and a backend framework (e.g., Flask). This API allows users to manage their tasks, including creating, reading, updating, and deleting (CRUD) operations.

Features
Create new tasks.
Read a list of tasks or individual task details.
Update existing tasks.
Delete tasks.
Mark tasks as complete/incomplete.
Getting Started
Prerequisites
Python 3
[Backend framework] i.e Flask
virtual environment (venv)
gunicorn for production
pip (Python package installer)
Installation
Clone the repository:

git clone https://github.com/Duckity6210/TODO-LIST.git

cd todos-api

I.P Adress where API is running

http://127.0.0.1:5000

WELCOME MESSAGE

curl http://localhost:5000

GET ALL TASKS

curl -X GET http://127.0.0.1:5000/tasks

GET TASK BY ID

curl -X GET http://127.0.0.1:5000/tasks/{task_id}

POST NEW TASK

curl -X POST http://127.0.0.1:5000/tasks -H "Content-Type: application/json" -d '{"title": "{title}"}'

DELETE TASK

curl -X DELETE http://127.0.0.1:5000/tasks/{task_id}

PUT TASK

curl -X PUT http://127.0.0.1:5000/tasks/{1} -H "Content-Type: application/json" -d '{"title": "title", "done": true}'

implement filtering and sorting

Get All Tasks (No Filters or Sorting):

curl -X GET "http://127.0.0.1:5000/tasks"

Filter by Completion Status (done=true):

curl -X GET "http://127.0.0.1:5000/tasks?done=true"

Sort by Task Title in Ascending Order:

curl -X GET "http://127.0.0.1:5000/tasks?sort_by=title&sort_order=asc"

Sort by Task ID in Descending Order

curl -X GET "http://127.0.0.1:5000/tasks?sort_by=id&sort_order=desc"

Combine Filtering and Sorting: To filter for completed tasks and sort by title in ascending order:

curl -X GET "http://127.0.0.1:5000/tasks?done=true&sort_by=title&sort_order=asc"

USER REGISTRATION

curl -X POST http://127.0.0.1:5000/register -H "Content-Type: application/json" -d '{"username": "PRISCA", "password": "37890524"}'

DEPLOYED PAGE UNDERWAY
