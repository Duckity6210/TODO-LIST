# iport require modules

import os
import Flask from flask
import jsonify
import request

app = Flask(__name__)

# Root route
@app.route('/')
def home():
    return "Todo Api - Yout Task List Manager"

if __name__ == "_main_":
    app.run(debug=True)

#  in app-memory storage
todos = [
    {"id": 1, "task": "Learn Python", "completed": True},
    {"id": 2, "task": "Build a Todo API", "completed": True}
]


# Get todo items
{
  "data": [
    {
      "id": 1,
      "title": "Pay bills",
      "description": "Electricity, Water, Rent"
    },
    {
      "id": 2,
      "title": "Savings an Investments",
      "description": "Cooperative bank, Hazina sacco"
    }
  ],
  "page": 1,
  "limit": 5,
  "total": 2
}

# Create a new todo
POST /todos
{
  "title": "Update notes",
  "description": "Basic maths, Calculus"
}

# Get a single todo by id
@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if todo:
        return jsonify(todo), 200
    else:
        return jsonify({"error": "Todo not found"}), 404

# Update a todo
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if todo:
        todo['task'] = data.get('task', todo['task'])
        todo['completed'] = data.get('completed', todo['completed'])
        return jsonify(todo), 200
    else:
        return jsonify({"error": "Todo not found"}), 404

# Delete a todo
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t['id'] != todo_id]
    return '', 204
