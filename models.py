from datetime import datetime
from app import db

class CallLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    call_sid = db.Column(db.String(64), unique=True, nullable=False)
    caller_number = db.Column(db.String(20))
    caller_input = db.Column(db.Text)
    bot_response = db.Column(db.Text)
    duration = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20))
    language = db.Column(db.String(10), default='en-US')  # Add language tracking

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)
    translations = db.relationship('ProductTranslation', backref='product', lazy=True)

class ProductTranslation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    language = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    customer_name = db.Column(db.String(100))
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    estimated_delivery = db.Column(db.DateTime)
    language = db.Column(db.String(10), default='en-US')  # Add language preference

class SupportedLanguage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)  # e.g., 'en-US', 'es-ES'
    name = db.Column(db.String(50), nullable=False)  # e.g., 'English (US)', 'Spanish (Spain)'
    voice_id = db.Column(db.String(50))  # ElevenLabs voice ID for this language
    active = db.Column(db.Boolean, default=True)