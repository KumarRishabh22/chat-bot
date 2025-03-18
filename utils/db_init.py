import os
import sys
import json
from datetime import datetime

# Add parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import Product, Order

def load_mock_data():
    try:
        # Read mock data
        with open('data/mock_data.json', 'r') as f:
            data = json.load(f)

        # Add products
        for product_data in data['products']:
            product = Product(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                stock=product_data['stock']
            )
            db.session.add(product)

        # Add orders
        for order_data in data['orders']:
            order = Order(
                order_number=order_data['order_number'],
                customer_name=order_data['customer_name'],
                status=order_data['status'],
                created_at=datetime.fromisoformat(order_data['created_at'].replace('Z', '+00:00')),
                estimated_delivery=datetime.fromisoformat(order_data['estimated_delivery'].replace('Z', '+00:00'))
            )
            db.session.add(order)

        db.session.commit()
        print("Mock data loaded successfully")

    except Exception as e:
        print(f"Error loading mock data: {e}")
        db.session.rollback()
        raise

if __name__ == "__main__":
    with app.app_context():
        # First ensure tables exist
        db.create_all()
        # Then load mock data
        load_mock_data()