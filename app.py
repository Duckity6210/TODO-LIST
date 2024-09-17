from flask import Flask, jsonify, request

app = Flask(__name__)

# memory storage

todos = [
    {"id": 1, "task": "Learn Python", "completed": False},
    {"id": 2, "task": "Build a Todo API", "completed": False}
]


# Get all todos
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos), 200

# Create a new todo
@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    todo = {
        'id': len(todos) + 1,
        'task': data['task'],
        'completed': False
    }
    todos.append(todo)
    return jsonify(todo), 201

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

# Root route
@app.route('/')
def home():
    return "Todo Api - Yout Task List Manager"

if __name__ == "_main_":
    app.run(debug=True)
