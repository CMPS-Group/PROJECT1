from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Session, Vehicle, InventoryLog, Order, OrderItem
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

@seller_bp.route('/vehicles/<int:vehicle_id>/inventory', methods=['PUT'])
@jwt_required()
@role_required('seller')
def update_inventory(vehicle_id):
    data = request.get_json()
    if not isinstance(data.get('inventory'), int) or data['inventory'] < 0:
        return jsonify({"message": "Invalid inventory value"}), 400
    user_id = get_jwt_identity()
    session = Session()
    vehicle = session.query(Vehicle).filter_by(id=vehicle_id, seller_id=user_id).first()
    if not vehicle:
        session.close()
        return jsonify({"message": "Vehicle not found or access denied"}), 404
    old_quantity = vehicle.inventory
    vehicle.inventory = data['inventory']
    log = InventoryLog(vehicle_id=vehicle_id, user_id=user_id, old_quantity=old_quantity, new_quantity=data['inventory'])
    session.add(log)
    session.commit()
    session.close()
    return jsonify({"message": "Inventory updated"})

@seller_bp.route('/inventory/alerts', methods=['GET'])
@jwt_required()
@role_required('seller')
def get_low_stock_alerts():
    threshold = request.args.get('threshold', default=10, type=int)
    user_id = get_jwt_identity()
    session = Session()
    vehicles = session.query(Vehicle).filter(Vehicle.seller_id == user_id, Vehicle.inventory <= threshold).all()
    session.close()
    return jsonify([{
        'id': v.id,
        'name': v.name,
        'inventory': v.inventory,
        'threshold': threshold
    } for v in vehicles])

@seller_bp.route('/inventory/restock-suggestions', methods=['GET'])
@jwt_required()
@role_required('seller')
def get_restock_suggestions():
    user_id = get_jwt_identity()
    session = Session()
    # Simple heuristic: suggest restock if inventory < 20 and has been sold in last 30 days (simplified)
    from sqlalchemy import func
    from datetime import datetime, timedelta
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    sold_vehicles = session.query(OrderItem.vehicle_id, func.sum(OrderItem.quantity).label('total_sold')).\
        join(Order).filter(Order.status == 'completed', Order.created_at >= thirty_days_ago).\
        group_by(OrderItem.vehicle_id).all()
    sold_vehicle_ids = {v.vehicle_id: v.total_sold for v in sold_vehicles}
    vehicles = session.query(Vehicle).filter_by(seller_id=user_id).all()
    suggestions = []
    for v in vehicles:
        if v.inventory < 20 and v.id in sold_vehicle_ids:
            suggestions.append({
                'id': v.id,
                'name': v.name,
                'current_inventory': v.inventory,
                'suggested_restock': max(50 - v.inventory, 0),  # Suggest to bring to 50
                'recent_sales': sold_vehicle_ids[v.id]
            })
    session.close()
    return jsonify(suggestions)
