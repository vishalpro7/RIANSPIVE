from sqlalchemy.orm import Session
from sqlalchemy import func

from models.user_model import User
from models.product_model import Product
from models.order_model import Order


def get_dashboard(db : Session):

    total_users = db.query(
        func.count(User.id)
    ).scalar()


    total_products = db.query(
        func.count(Product.id)
    ).scalar()


    total_orders = db.query(
        func.count(Order.id)
    ).scalar()


    pending_orders = db.query(
        func.count(Order.id)
    ).filter(
        Order.status == "Pending"
    ).scalar()


    delivered_orders = db.query(
        func.count(Order.id)
    ).filter(
        Order.status == "Delivered"
    ).scalar()


    cancelled_orders = db.query(
        func.count(Order.id)
    ).filter(
        Order.status == "Cancelled"
    ).scalar()


    total_revenue = (
        db.query(
            func.sum(Order.total_amount)
        ).scalar()
        or 0
    )


    return {

        "total_users" : total_users, 

        "total_products" : total_products, 

        "total_orders" : total_orders, 

        "pending_orders" : pending_orders, 

        "delivered_orders" : delivered_orders, 

        "cancelled_orders" : cancelled_orders, 

        "total_revenue" : total_revenue
    }

