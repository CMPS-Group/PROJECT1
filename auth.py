from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from functools import wraps
from models import Session, User

def register_user(username, password, role):
    session = Session()
    if session.query(User).filter_by(username=username).first():
        session.close()
        return False, "Username already exists"
    user = User(username=username, role=role)
    user.set_password(password)
    session.add(user)
    session.commit()
    session.close()
    return True, "User registered successfully"

def authenticate_user(username, password):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    if user and user.check_password(password):
        return user
    return None

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            session = Session()
            user = session.query(User).filter_by(id=current_user_id).first()
            session.close()
            if not user or user.role != required_role:
                return jsonify({"message": "Access denied"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
