from sqlalchemy.orm import Session
from sqlalchemy import func

from models.product_model import Product
from models.order_item_model import OrderItem

def get_analytics(
        db : Session
):
    
    results = (
        db.query(
            Product.name, 
            func.sum(OrderItem.quantity)
        )

        .join(
            OrderItem, 
            Product.id == OrderItem.product_id
        )

        .group_by(
            Product.id, 

            Product.name
        )

        .order_by(
            func.sum(OrderItem.quantity).desc()
        )

        .limit(5)

        .all()
    )

    best_products = [
        {
            "product" : name, 

            "quantity_sold" : quantity
        }

        for name, quantity in results
    ]

    return {
        "best_selling_products" : best_products
    }