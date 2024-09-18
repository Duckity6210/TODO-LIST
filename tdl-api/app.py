from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['JWT_SECRET_KEY'] = 'supersecret'  # Change this for production
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["20 per day", "10 per hour"]
)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Create Database
@app.before_first_request
def create_tables():
    db.create_all()

# User Registration
@app.route('/register', methods=['POST'])
@limiter.limit("10 per hour")
def register():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(name=name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# User Login
@app.route('/login', methods=['POST'])
@limiter.limit("20 per hour")
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
        return jsonify({'token': token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

# Create a Todo Item
@app.route('/todos', methods=['POST'])
@jwt_required()
@limiter.limit("50 per day")
def create_todo():
    data = request.get_json()
    title = data['title']
    description = data['description']
    user_id = get_jwt_identity()

    new_todo = TodoItem(title=title, description=description, user_id=user_id)
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({
        'id': new_todo.id,
        'title': new_todo.title,
        'description': new_todo.description
    }), 201

# Update a Todo Item
@app.route('/todos/<int:id>', methods=['PUT'])
@jwt_required()
def update_todo(id):
    data = request.get_json()
    user_id = get_jwt_identity()
    
    todo = TodoItem.query.filter_by(id=id, user_id=user_id).first()
    if not todo:
        return jsonify({'message': 'Todo not found'}), 404

    todo.title = data['title']
    todo.description = data['description']
    db.session.commit()

    return jsonify({'message': 'Todo updated successfully'}), 200

# Delete a Todo Item
@app.route('/todos/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_todo(id):
    user_id = get_jwt_identity()
    
    todo = TodoItem.query.filter_by(id=id, user_id=user_id).first()
    if not todo:
        return jsonify({'message': 'Todo not found'}), 404

    db.session.delete(todo)
    db.session.commit()

    return jsonify({'message': 'Todo deleted successfully'}), 200

# Get Todos with Pagination, Filtering, and Sorting
@app.route('/todos', methods=['GET'])
@jwt_required()
def get_todos():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    sort_by = request.args.get('sort_by', 'id', type=str)
    order = request.args.get('order', 'asc', type=str)
    title_filter = request.args.get('title', '', type=str)

    query = TodoItem.query.filter_by(user_id=user_id)
    
    if title_filter:
        query = query.filter(TodoItem.title.contains(title_filter))
    
    if order == 'desc':
        query = query.order_by(db.desc(sort_by))
    else:
        query = query.order_by(sort_by)

    todos = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'todos': [{
            'id': todo.id,
            'title': todo.title,
            'description': todo.description
        } for todo in todos.items],
        'total_pages': todos.pages,
        'current_page': todos.page,
        'total_items': todos.total
    }), 200

if __name__ == '_main_':
    app.run(debug=True)
