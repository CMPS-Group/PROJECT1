from werkzeug.exceptions import UnprocessableEntity
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
# Register blueprints
app.register_blueprint(buyer_bp, url_prefix='/buyer')
app.register_blueprint(seller_bp, url_prefix='/seller')
app.register_blueprint(admin_bp, url_prefix='/admin')

# Global error handler for 422 Unprocessable Entity
@app.errorhandler(UnprocessableEntity)
def handle_422(e):
    return jsonify({"message": "Invalid input"}), 400

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    role = data.get('role', '').strip().lower()
    import html
    username = html.escape(username)
    role = html.escape(role)
    # Basic checks
    if not isinstance(username, str) or not username or len(username) > 32:
        return jsonify({"message": "Invalid username"}), 400
    if not isinstance(password, str) or not password or len(password) < 8 or len(password) > 128:
        return jsonify({"message": "Invalid password"}), 400
    if role not in {"admin", "seller", "buyer"}:
        return jsonify({"message": "Invalid role"}), 400
    success, message = register_user(username, password, role)
    if success:
        return jsonify({"message": message}), 201
    return jsonify({"message": message}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    import html
    username = html.escape(username)
    # Basic checks
    if not isinstance(username, str) or not username or len(username) > 32:
        return jsonify({"message": "Invalid username"}), 400
    if not isinstance(password, str) or not password or len(password) < 8 or len(password) > 128:
        return jsonify({"message": "Invalid password"}), 400
    user = authenticate_user(username, password)
    if user:
        access_token = create_access_token(identity=user.username)
        return jsonify({"access_token": access_token, "role": user.role}), 200
    return jsonify({"message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(debug=True)
