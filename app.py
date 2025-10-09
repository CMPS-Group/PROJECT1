from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from auth import register_user, authenticate_user
from routes.buyer import buyer_bp
from routes.seller import seller_bp
from routes.admin import admin_bp
from models import Session

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change in production
jwt = JWTManager(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not all(k in data for k in ('username', 'password', 'role')):
        return jsonify({"message": "Missing required fields"}), 400
    if data['role'] not in ['buyer', 'seller', 'admin']:
        return jsonify({"message": "Invalid role"}), 400
    success, message = register_user(data['username'].strip(), data['password'], data['role'])
    if success:
        return jsonify({"message": message}), 201
    return jsonify({"message": message}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ('username', 'password')):
        return jsonify({"message": "Missing credentials"}), 400
    user = authenticate_user(data['username'].strip(), data['password'])
    if user:
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token, role=user.role)
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # For JWT, logout is client-side, but we can return success
    return jsonify({"message": "Logged out successfully"}), 200

app.register_blueprint(buyer_bp, url_prefix='/buyer')
app.register_blueprint(seller_bp, url_prefix='/seller')
app.register_blueprint(admin_bp, url_prefix='/admin')

if __name__ == '__main__':
    app.run(debug=True)
