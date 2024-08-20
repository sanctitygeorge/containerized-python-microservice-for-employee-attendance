from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='staff')
    first_name = db.Column(db.String(100), nullable=False)  
    last_name = db.Column(db.String(1000), nullable=False)   
    department = db.Column(db.String(100), nullable=True) 
    created_at = db.Column(db.DateTime, default=datetime.now(datetime))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Attendance(db.Model):
    __tablename__ = 'attendance'  # Explicitly set table name if needed
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='attendances')
    
    def __repr__(self):
        return f"<Attendance {self.date} - {self.user.username}>"