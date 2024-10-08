from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and password hashing
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# User model to store user credentials
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

# Initialize the database
with app.app_context():
    db.create_all()

#welcome.route

@app.route('/')
def welcome():
    return jsonify({"message": "Todo API - Your Task List Manager"})

# User registration route
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    if not data or not 'username' in data or not 'password' in data:
        return jsonify({'error': 'Username and password are required'}), 400

    # Check if username already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409

    # Hash the password before storing
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # Create a new user and save to the database
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


# In-memory database for demonstration purposes
tasks = [
    {'id': 1, 'title': 'Submit Assignment', 'done': False},
    {'id': 2, 'title': 'Pay Electricity Bill', 'done': False},
    {'id': 3, 'title': 'Deposit Money', 'done': False},
    {'id': 4, 'title': 'Do Laundry', 'done': False}
]

# GET /tasks route with filtering and sorting
@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Get query parameters for filtering and sorting
    done_filter = request.args.get('done')  # Filter by completion status
    sort_by = request.args.get('sort_by')   # Sorting field (id, title, done)
    sort_order = request.args.get('sort_order', 'asc')  # Sorting order (asc or desc)

    # Start with all tasks
    filtered_tasks = tasks

    # Filtering logic: filter by completion status
    if done_filter is not None:
        done_filter = done_filter.lower() == 'true'
        filtered_tasks = [task for task in tasks if task['done'] == done_filter]

    # Sorting logic: sort by field and order
    if sort_by:
        reverse = (sort_order == 'desc')
        if sort_by in ['id', 'title', 'done']:
            filtered_tasks = sorted(filtered_tasks, key=lambda x: x[sort_by], reverse=reverse)

    return jsonify({'tasks': filtered_tasks})

# GET specific task by id

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'task': task})

# POST - create a new task

@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        return jsonify({'error': 'Bad request'}), 400
    new_task = {
        'id': tasks[-1]['id'] + 1 if tasks else 1,
        'title': request.json['title'],
        'done': False
    }
    tasks.append(new_task)
    return jsonify({'task': new_task}), 201

# PUT - update a task

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    if not request.json:
        return jsonify({'error': 'Bad request'}), 400
    task['title'] = request.json.get('title', task['title'])
    task['done'] = request.json.get('done', task['done'])
    return jsonify({'task': task})

# DELETE - delete a task

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({'result': 'Task deleted'})

if __name__ == '__main__':
    app.run(debug=True)

