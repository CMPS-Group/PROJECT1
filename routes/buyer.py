from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Session, Vehicle, CartItem, Order, OrderItem, Discount, InventoryLog
from auth import role_required

buyer_bp = Blueprint('buyer', __name__)

@buyer_bp.route('/vehicles', methods=['GET'])
@jwt_required()
@role_required('buyer')
def browse_vehicles():
    session = Session()
    vehicles = session.query(Vehicle).all()
    session.close()
    return jsonify([{
        'id': v.id,
        'name': v.name,
        'description': v.description,
        'price': v.price,
        'inventory': v.inventory
    } for v in vehicles])

@buyer_bp.route('/cart', methods=['POST'])
@jwt_required()
@role_required('buyer')
def add_to_cart():
    data = request.get_json()
    if not isinstance(data.get('vehicle_id'), int) or not isinstance(data.get('quantity'), int) or data['quantity'] <= 0:
        return jsonify({"message": "Invalid input"}), 400
    user_id = get_jwt_identity()
    session = Session()
    vehicle = session.query(Vehicle).filter_by(id=data['vehicle_id']).first()
    if not vehicle or vehicle.inventory < data['quantity']:
        session.close()
        return jsonify({"message": "Invalid vehicle or insufficient inventory"}), 400
    cart_item = CartItem(user_id=user_id, vehicle_id=data['vehicle_id'], quantity=data['quantity'])
    session.add(cart_item)
    session.commit()
    session.close()
    return jsonify({"message": "Added to cart"})

@buyer_bp.route('/cart', methods=['GET'])
@jwt_required()
@role_required('buyer')
def view_cart():
    user_id = get_jwt_identity()
    session = Session()
    items = session.query(CartItem).filter_by(user_id=user_id).all()
    cart = []
    total = 0
    for item in items:
        vehicle = session.query(Vehicle).filter_by(id=item.vehicle_id).first()
        if vehicle:
            cart.append({
                'vehicle_id': item.vehicle_id,
                'name': vehicle.name,
                'quantity': item.quantity,
                'price': vehicle.price,
                'subtotal': item.quantity * vehicle.price
            })
            total += item.quantity * vehicle.price
    session.close()
    return jsonify({'cart': cart, 'total': total})

@buyer_bp.route('/checkout', methods=['POST'])
@jwt_required()
@role_required('buyer')
def checkout():
    data = request.get_json()
    payment_info = data.get('payment_info')  # Mock payment validation
    discount_code = data.get('discount_code')
    if not payment_info or not isinstance(payment_info, str) or len(payment_info.strip()) < 10:  # Simple mock
        return jsonify({"message": "Invalid payment info"}), 400
    user_id = get_jwt_identity()
    session = Session()
    items = session.query(CartItem).filter_by(user_id=user_id).all()
    if not items:
        session.close()
        return jsonify({"message": "Cart is empty"}), 400
    total = 0
    discount_amount = 0
    if discount_code and isinstance(discount_code, str):
        discount = session.query(Discount).filter_by(code=discount_code.strip()).first()
        if discount:
            discount_amount = discount.percentage / 100
    order_items = []
    for item in items:
        vehicle = session.query(Vehicle).filter_by(id=item.vehicle_id).first()
        if vehicle.inventory < item.quantity:
            session.close()
            return jsonify({"message": f"Insufficient inventory for {vehicle.name}"}), 400
        subtotal = item.quantity * vehicle.price
        total += subtotal
        order_items.append(OrderItem(vehicle_id=item.vehicle_id, quantity=item.quantity, price=vehicle.price))
        old_quantity = vehicle.inventory
        vehicle.inventory -= item.quantity
        # Log inventory change (user_id is the seller's id)
        log = InventoryLog(vehicle_id=item.vehicle_id, user_id=vehicle.seller_id, old_quantity=old_quantity, new_quantity=vehicle.inventory)
        session.add(log)
    total -= total * discount_amount
    order = Order(user_id=user_id, total=total)
    session.add(order)
    session.flush()  # Get order.id
    for oi in order_items:
        oi.order_id = order.id
        session.add(oi)
    session.query(CartItem).filter_by(user_id=user_id).delete()
    session.commit()
    order_id = order.id
    session.close()
    return jsonify({"message": "Order placed successfully", "order_id": order_id, "total": total})

@buyer_bp.route('/orders', methods=['GET'])
@jwt_required()
@role_required('buyer')
def get_orders():
    user_id = get_jwt_identity()
    session = Session()
    orders = session.query(Order).filter_by(user_id=user_id).all()
    order_list = []
    for order in orders:
        items = session.query(OrderItem).filter_by(order_id=order.id).all()
        item_list = [{
            'vehicle_id': i.vehicle_id,
            'name': i.vehicle.name,
            'quantity': i.quantity,
            'price': i.price
        } for i in items]
        order_list.append({
            'id': order.id,
            'total': order.total,
            'status': order.status,
            'items': item_list
        })
    session.close()
    return jsonify(order_list)
