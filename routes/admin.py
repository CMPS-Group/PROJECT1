from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Session, Order, User, Discount
from auth import role_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/orders', methods=['GET'])
@jwt_required()
@role_required('admin')
def monitor_orders():
    session = Session()
    orders = session.query(Order).all()
    session.close()
    return jsonify([{
        'id': o.id,
        'user_id': o.user_id,
        'total': o.total,
        'status': o.status
    } for o in orders])

@admin_bp.route('/discounts', methods=['POST'])
@jwt_required()
@role_required('admin')
def add_discount():
    data = request.get_json()
    admin_id = get_jwt_identity()  # Assuming admin is user
    session = Session()
    discount = Discount(
        code=data['code'],
        percentage=data['percentage'],
        admin_id=admin_id
    )
    session.add(discount)
    session.commit()
    session.close()
    return jsonify({"message": "Discount added"})

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@role_required('admin')
def list_users():
    session = Session()
    users = session.query(User).all()
    session.close()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'role': u.role
    } for u in users])

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_user(user_id):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        session.close()
        return jsonify({"message": "User not found"}), 404
    session.delete(user)
    session.commit()
    session.close()
    return jsonify({"message": "User deleted"})

@admin_bp.route('/users/<int:user_id>/role', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_user_role(user_id):
    data = request.get_json()
    new_role = data.get('role')
    if not new_role or new_role not in ['buyer', 'seller', 'admin']:
        return jsonify({"message": "Invalid role"}), 400
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        session.close()
        return jsonify({"message": "User not found"}), 404
    user.role = new_role
    session.commit()
    session.close()
    return jsonify({"message": "User role updated"})
