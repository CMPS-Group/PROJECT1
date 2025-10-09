from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from auth import register_user, authenticate_user
from routes.buyer import buyer_bp
from routes.seller import seller_bp
from routes.admin import admin_bp
from models import engine, Base

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change in production
jwt = JWTManager(app)

# Create tables
Base.metadata.create_all(engine)

# Register blueprints
app.register_blueprint(buyer_bp, url_prefix='/buyer')
app.register_blueprint(seller_bp, url_prefix='/seller')
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    success, message = register_user(data['username'], data['password'], data['role'])
    if success:
        return jsonify({"message": message}), 201
    return jsonify({"message": message}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = authenticate_user(data['username'], data['password'])
    if user:
        access_token = create_access_token(identity=user.username)
        return jsonify({"access_token": access_token, "role": user.role}), 200
    return jsonify({"message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(debug=True)
