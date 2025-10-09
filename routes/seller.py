from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Session, Product
from auth import role_required

seller_bp = Blueprint('seller', __name__)

@seller_bp.route('/products', methods=['POST'])
@jwt_required()
@role_required('seller')
def add_product():
    data = request.get_json()
    if not isinstance(data.get('name'), str) or not data['name'].strip() or \
       not isinstance(data.get('price'), (int, float)) or data['price'] <= 0 or \
       not isinstance(data.get('inventory'), int) or data['inventory'] < 0:
        return jsonify({"message": "Invalid input"}), 400
    user_id = get_jwt_identity()
    session = Session()
    product = Product(
        name=data['name'].strip(),
        description=data.get('description', '').strip(),
        price=data['price'],
        inventory=data['inventory'],
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
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.inventory = data.get('inventory', product.inventory)
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
