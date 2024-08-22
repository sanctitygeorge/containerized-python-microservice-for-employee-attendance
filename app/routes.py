from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash, session
from app import db
from app.models import User, Attendance
from flask_jwt_extended import create_access_token, verify_jwt_in_request,jwt_required, get_jwt_identity
from datetime import datetime

bp = Blueprint('routes', __name__)

# Home Page
@bp.route('/', methods=['GET'])
def home():
    return "<h1> Welcome to the Attendance Portal</h1>"

# User Registration
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            department = data.get('department')
        else:
            username = request.form.get('username')
            password = request.form.get('password')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            department = request.form.get('department')
        
        if not all([username, password, first_name, last_name]):
            response = {"message": "Missing required fields"}
            return jsonify(response), 400 if request.content_type == 'application/json' else render_template('register.html', error="Missing required fields")
        
        if User.query.filter_by(username=username).first():
            response = {"message": "User already exists"}
            return jsonify(response), 400 if request.content_type == 'application/json' else render_template('register.html', error="User already exists")
        
        user = User(username=username, first_name=first_name, last_name=last_name, department=department)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        response = {"message": "User registered successfully"}
        if request.content_type == 'application/json':
            return jsonify(response), 201
        else:
            flash("User registered successfully")
            return redirect(url_for('routes.login'))
    
    return render_template('register.html')


# User Login
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
        else:
            username = request.form.get('username')
            password = request.form.get('password')
        
        if not all([username, password]):
            response = {"message": "Missing required fields"}
            if request.content_type == 'application/json':
                return jsonify(response), 400
            else:
                return render_template('login.html', error="Missing required fields")
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            access_token = create_access_token(identity={'username': user.username, 'role': user.role})
            session['access_token'] = access_token  # Store JWT in session
            if request.content_type == 'application/json':
                response = {"access_token": access_token}
                return jsonify(response), 200
            else:
                # Redirect with token in query (for debugging)
                return redirect(url_for('routes.mark_attendance') + f'?token={access_token}')
        else:
            response = {"message": "Invalid credentials"}
            if request.content_type == 'application/json':
                return jsonify(response), 401
            else:
                return render_template('login.html', error="Invalid credentials")
    
    return render_template('login.html')


# Mark Attendance
@bp.route('/attendance', methods=['GET', 'POST'])
@jwt_required()  # Use JWT required to protect this route
def mark_attendance():
    # Make sure to verify JWT in the request context
    try:
        verify_jwt_in_request()
        user_identity = get_jwt_identity()
        user = User.query.filter_by(username=user_identity['username']).first()
        
        if not user:
            if request.is_json:
                return jsonify({"message": "User not found"}), 404
            else:
                return render_template('mark_attendance.html', error="User not found")

        attendance = Attendance(user=user)
        db.session.add(attendance)
        db.session.commit()
        
        if request.is_json:
            return jsonify({"message": "Attendance marked successfully"}), 200
        else:
            return render_template('mark_attendance.html', success="Attendance marked successfully")
    except Exception as e:
        if request.is_json:
            return jsonify({"message": str(e)}), 401
        else:
            return render_template('mark_attendance.html', error=str(e))


# Admin - Create a new user
@bp.route('/admin/users', methods=['POST'])
@jwt_required()
def create_user():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"message": "Admin access required"}), 403

    if request.content_type == 'application/json':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        department = data.get('department')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        department = request.form.get('department')

    if not all([username, password, first_name, last_name]):
        response = {"message": "Missing required fields"}
        return jsonify(response), 400 if request.content_type == 'application/json' else render_template('admin_create_user.html', error="Missing required fields")
    
    if User.query.filter_by(username=username).first():
        response = {"message": "User already exists"}
        return jsonify(response), 400 if request.content_type == 'application/json' else render_template('admin_create_user.html', error="User already exists")
    
    user = User(
        username=username,
        first_name=first_name,
        last_name=last_name,
        department=department
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    response = {"message": "User created successfully"}
    return jsonify(response), 201 if request.content_type == 'application/json' else redirect(url_for('routes.get_users'))

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
    
    if request.content_type == 'application/json':
        data = request.get_json()
    else:
        data = {
            'username': request.form.get('username'),
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'department': request.form.get('department'),
            'password': request.form.get('password')
        }

    user.username = data.get('username', user.username)
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.department = data.get('department', user.department)
    if 'password' in data:
        user.set_password(data['password'])

    db.session.commit()

    return jsonify({"message": "User updated successfully"}), 200 if request.content_type == 'application/json' else redirect(url_for('routes.get_users'))

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
    
    if request.content_type == 'application/json':
        data = request.get_json()
    else:
        data = {'status': request.form.get('status')}

    attendance.status = data.get('status', attendance.status)
    db.session.commit()

    return jsonify({"message": "Attendance updated successfully"}), 200 if request.content_type == 'application/json' else redirect(url_for('routes.get_attendance'))

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
