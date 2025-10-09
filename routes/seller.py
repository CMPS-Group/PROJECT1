from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Session, Vehicle
from auth import role_required

seller_bp = Blueprint('seller', __name__)

@seller_bp.route('/vehicles', methods=['POST'])
@jwt_required()
@role_required('seller')
def add_vehicle():
    data = request.get_json()
    if not isinstance(data.get('name'), str) or not data['name'].strip() or \
       not isinstance(data.get('price'), (int, float)) or data['price'] <= 0 or \
       not isinstance(data.get('inventory'), int) or data['inventory'] < 0:
        return jsonify({"message": "Invalid input"}), 400
    user_id = get_jwt_identity()
    session = Session()
    vehicle = Vehicle(
        name=data['name'].strip(),
        description=data.get('description', '').strip(),
        price=data['price'],
        inventory=data['inventory'],
        seller_id=user_id
    )
    session.add(vehicle)
    session.commit()
    vehicle_id = vehicle.id
    session.close()
    return jsonify({"message": "Vehicle added", "vehicle_id": vehicle_id})

@seller_bp.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
@jwt_required()
@role_required('seller')
def edit_vehicle(vehicle_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    session = Session()
    vehicle = session.query(Vehicle).filter_by(id=vehicle_id, seller_id=user_id).first()
    if not vehicle:
        session.close()
        return jsonify({"message": "Vehicle not found or access denied"}), 404
    vehicle.name = data.get('name', vehicle.name)
    vehicle.description = data.get('description', vehicle.description)
    vehicle.price = data.get('price', vehicle.price)
    vehicle.inventory = data.get('inventory', vehicle.inventory)
    session.commit()
    session.close()
    return jsonify({"message": "Vehicle updated"})

@seller_bp.route('/vehicles', methods=['GET'])
@jwt_required()
@role_required('seller')
def list_vehicles():
    user_id = get_jwt_identity()
    session = Session()
    vehicles = session.query(Vehicle).filter_by(seller_id=user_id).all()
    session.close()
    return jsonify([{
        'id': v.id,
        'name': v.name,
        'description': v.description,
        'price': v.price,
        'inventory': v.inventory
    } for v in vehicles])
