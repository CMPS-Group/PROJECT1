from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    role = Column(String(20), nullable=False)  # 'buyer', 'seller', 'admin'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    inventory = Column(Integer, nullable=False)
    seller_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    seller = relationship('User')

class CartItem(Base):
    __tablename__ = 'cart_items'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    user = relationship('User')
    product = relationship('Product')

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total = Column(Float, nullable=False)
    status = Column(String(20), default='pending')  # 'pending', 'completed', 'cancelled'

    user = relationship('User')
    items = relationship('OrderItem')

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    order = relationship('Order')
    product = relationship('Product')

class Discount(Base):
    __tablename__ = 'discounts'
    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True, nullable=False)
    percentage = Column(Float, nullable=False)
    admin_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    admin = relationship('User')

# Database setup
engine = create_engine('sqlite:///ecommerce.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
