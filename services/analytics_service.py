from sqlalchemy.orm import Session
from sqlalchemy import func

from models.product_model import Product
from models.order_item_model import OrderItem
from models.order_model import Order

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

def get_revenue_analytics(
        db : Session
):
    total_revenue = (
        db.query(
            func.sum(Order.total_amount)
        )
        .scalar()
    )

    total_orders = (
        db.query(
            func.count(Order.id)
        )
        .scalar()
    )

    average_order_value = (
        db.query(
            func.avg(Order.total_amount)
        )
        .scalar()
    )

    return {
        "total_revenue" : total_revenue or 0, 
        "total_orders" : total_orders or 0, 
        "average_order_value" : average_order_value or 0
    }