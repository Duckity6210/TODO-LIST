from flask import Flask, jsonify, request, abort
from models import db, Task
from config import Config
import logging

# set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Create database
def create_tables():
    with app.app_context():
        db.create_all()

# Route: Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks]), 200

# Route: Get task by ID
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    if not task:
        abort(404, description="Task not found")
    return jsonify(task.to_dict()), 200

# Route: Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400, description="Title is required")
    
    task = Task(
        title=request.json['title'],
        description=request.json.get('description', ''),
        completed=request.json.get('completed', False)
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

# Route: Update a task by ID
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if not task:
        abort(404, description="Task not found")
    
    data = request.json
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    
    db.session.commit()
    return jsonify(task.to_dict()), 200

# Route: Delete a task by ID
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        abort(404, description="Task not found")
    
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": error.description}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": error.description}), 400

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
