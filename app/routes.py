from flask import Blueprint, jsonify, request
from app import db
from app.models import User, Attendance
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime

bp = Blueprint('routes', __name__)

# User Registration
@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    department = data.get('department')
    
    if not all([username, password, first_name, last_name]):
        return jsonify({"message": "Missing required fields"}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 400
    
    user = User(username=username, first_name=first_name, last_name=last_name, department=department)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 201

# User Login
@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not all([username, password]):
        return jsonify({"message": "Missing required fields"}), 400
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        access_token = create_access_token(identity={'username': user.username, 'role': user.role})
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials"}), 401


# Mark Attendance
@bp.route('/attendance', methods=['POST'])
@jwt_required()
def mark_attendance():
    user_identity = get_jwt_identity()
    user = User.query.filter_by(username=user_identity['username']).first()
    
    attendance = Attendance(user=user)
    db.session.add(attendance)
    db.session.commit()
    
    return jsonify({"message": "Attendance marked successfully"}), 200


# Admin - Create a new user
@bp.route('/admin/users', methods=['POST'])
@jwt_required()
def create_user():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"message": "Admin access required"}), 403

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    department = data.get('department')

    if not all([username, password, first_name, last_name]):
        return jsonify({"message": "Missing required fields"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 400

    user = User(
        username=username,
        first_name=first_name,
        last_name=last_name,
        department=department
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

# Admin - Retrieve all users
@bp.route('/admin/users', methods=['GET'])
@jwt_required()
def get_users():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"message": "Admin access required"}), 403

    users = User.query.all()
    users_list = [{
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "department": user.department,
        "role": user.role,
        "created_at": user.created_at
    } for user in users]

    return jsonify(users=users_list), 200

# Admin - Update a user
@bp.route('/admin/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"message": "Admin access required"}), 403

    user = User.query.get_or_404(user_id)
    data = request.get_json()

    user.username = data.get('username', user.username)
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.department = data.get('department', user.department)
    if 'password' in data:
        user.set_password(data['password'])

    db.session.commit()

    return jsonify({"message": "User updated successfully"}), 200

# Admin - Delete a user
@bp.route('/admin/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"message": "Admin access required"}), 403

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200

# Admin - Retrieve all attendance records
@bp.route('/admin/attendance', methods=['GET'])
@jwt_required()
def get_attendance():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"message": "Admin access required"}), 403

    attendance_records = Attendance.query.all()
    attendance_list = [{
        "id": record.id,
        "username": record.user.username,
        "date": record.date,
        "status": record.status
    } for record in attendance_records]

    return jsonify(attendance=attendance_list), 200

# Admin - Update an attendance record
@bp.route('/admin/attendance/<int:attendance_id>', methods=['PUT'])
@jwt_required()
def update_attendance(attendance_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"message": "Admin access required"}), 403

    attendance = Attendance.query.get_or_404(attendance_id)
    data = request.get_json()

    attendance.status = data.get('status', attendance.status)
    db.session.commit()

    return jsonify({"message": "Attendance updated successfully"}), 200

# Admin - Delete an attendance record
@bp.route('/admin/attendance/<int:attendance_id>', methods=['DELETE'])
@jwt_required()
def delete_attendance(attendance_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"message": "Admin access required"}), 403

    attendance = Attendance.query.get_or_404(attendance_id)
    db.session.delete(attendance)
    db.session.commit()

    return jsonify({"message": "Attendance record deleted successfully"}), 200