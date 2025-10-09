from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Session, Product, InventoryLog, Order, OrderItem
from auth import role_required

seller_bp = Blueprint('seller', __name__)

@seller_bp.route('/products', methods=['POST'])
@jwt_required()
@role_required('seller')
def add_product():
    data = request.get_json()
    name = data.get('name', '').strip()
    description = data.get('description', '').strip()
    price = data.get('price')
    inventory = data.get('inventory')
    import html
    name = html.escape(name)
    description = html.escape(description)
    # Basic checks
    if not isinstance(name, str) or not name or len(name) > 64:
        return jsonify({"message": "Invalid product name"}), 400
    if not isinstance(description, str) or len(description) > 256:
        return jsonify({"message": "Invalid product description"}), 400
    if not isinstance(price, (int, float)) or price <= 0 or price > 100000:
        return jsonify({"message": "Invalid price"}), 400
    if not isinstance(inventory, int) or inventory < 0 or inventory > 100000:
        return jsonify({"message": "Invalid inventory value"}), 400
    user_id = get_jwt_identity()
    session = Session()
    product = Product(
        name=name,
        description=description,
        price=price,
        inventory=inventory,
        seller_id=user_id
    )
    session.add(product)
    session.commit()
    product_id = product.id
    session.close()
    return jsonify({"message": "Product added", "product_id": product_id})

@seller_bp.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
@role_required('seller')
def edit_product(product_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    session = Session()
    product = session.query(Product).filter_by(id=product_id, seller_id=user_id).first()
    if not product:
        session.close()
        return jsonify({"message": "Product not found or access denied"}), 404
    name = data.get('name', product.name).strip()
    description = data.get('description', product.description).strip()
    price = data.get('price', product.price)
    inventory = data.get('inventory', product.inventory)
    import html
    name = html.escape(name)
    description = html.escape(description)
    # Basic checks
    if not isinstance(name, str) or not name or len(name) > 64:
        session.close()
        return jsonify({"message": "Invalid product name"}), 400
    if not isinstance(description, str) or len(description) > 256:
        session.close()
        return jsonify({"message": "Invalid product description"}), 400
    if not isinstance(price, (int, float)) or price <= 0 or price > 100000:
        session.close()
        return jsonify({"message": "Invalid price"}), 400
    if not isinstance(inventory, int) or inventory < 0 or inventory > 100000:
        session.close()
        return jsonify({"message": "Invalid inventory value"}), 400
    product.name = name
    product.description = description
    product.price = price
    product.inventory = inventory
    session.commit()
    session.close()
    return jsonify({"message": "Product updated"})

@seller_bp.route('/products', methods=['GET'])
@jwt_required()
@role_required('seller')
def list_products():
    user_id = get_jwt_identity()
    session = Session()
    products = session.query(Product).filter_by(seller_id=user_id).all()
    session.close()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': p.price,
        'inventory': p.inventory
    } for p in products])

@seller_bp.route('/products/<int:product_id>/inventory', methods=['PUT'])
@jwt_required()
@role_required('seller')
def update_inventory(product_id):
    data = request.get_json()
    if not isinstance(data.get('inventory'), int) or data['inventory'] < 0:
        return jsonify({"message": "Invalid inventory value"}), 400
    user_id = get_jwt_identity()
    session = Session()
    product = session.query(Product).filter_by(id=product_id, seller_id=user_id).first()
    if not product:
        session.close()
        return jsonify({"message": "Product not found or access denied"}), 404
    old_quantity = product.inventory
    product.inventory = data['inventory']
    log = InventoryLog(product_id=product_id, user_id=user_id, old_quantity=old_quantity, new_quantity=data['inventory'])
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
    products = session.query(Product).filter(Product.seller_id == user_id, Product.inventory <= threshold).all()
    session.close()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'inventory': p.inventory,
        'threshold': threshold
    } for p in products])

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
    sold_products = session.query(OrderItem.product_id, func.sum(OrderItem.quantity).label('total_sold')).\
        join(Order).filter(Order.status == 'completed', Order.created_at >= thirty_days_ago).\
        group_by(OrderItem.product_id).all()
    sold_product_ids = {p.product_id: p.total_sold for p in sold_products}
    products = session.query(Product).filter_by(seller_id=user_id).all()
    suggestions = []
    for p in products:
        if p.inventory < 20 and p.id in sold_product_ids:
            suggestions.append({
                'id': p.id,
                'name': p.name,
                'current_inventory': p.inventory,
                'suggested_restock': max(50 - p.inventory, 0),  # Suggest to bring to 50
                'recent_sales': sold_product_ids[p.id]
            })
    session.close()
    return jsonify(suggestions)
