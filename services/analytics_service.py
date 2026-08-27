from sqlalchemy.orm import Session
from sqlalchemy import func

from models.product_model import Product
from models.order_item_model import OrderItem
from models.order_model import Order
from datetime import datetime, timedelta

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

def get_time_based_revenue(
        db : Session
):
    now = datetime.now()

    start_of_day = datetime(
        now.year, 
        now.month, 
        now.day
    )

    start_of_month = datetime(
        now.year, 
        now.month, 
        1
    )

    today_revenue = (
        db.query(
            func.sum(Order.total_amount)
        )
        .filter(
            Order.created_at >= start_of_day
        )
        .scalar()
    )

    month_revenue = (
        db.query(
            func.sum(Order.total_amount)
        )
        .filter(
            Order.created_at >= start_of_month
        )
        .scalar()
    )

    return {
        "today_revenue" : today_revenue or 0, 
        "month_revenue" : month_revenue or 0
    }

def get_date_based_analytics(
        db : Session,
        start_date : datetime, 
        end_date : datetime
):
    revenue = (
        db.query(
            func.sum(Order.total_amount)
        )
        .filter(Order.created_at >= start_date,
                Order.created_at <= end_date)
        .scalar()
    )

    return {
        "start_date" : start_date, 
        "end_date" : end_date, 
        "revenue" : revenue or 0
    }

def get_revenue_by_status(
        db : Session
):
    results = (
        db.query(
            Order.status,
            func.sum(Order.total_amount)
        )
        .group_by(Order.status)
        .all()
    )


    revenue_by_status = [
        {
            "status" : status, 
            "revenue" : revenue or 0
        }
        for status, revenue in results
    ]

    return {
        "revenue_by_status" : revenue_by_status
    }

def get_orders_by_status(
        db : Session
):
    results = (
        db.query(
            Order.status, 
            func.sum(Order.id)
        )
        .group_by(Order.status)
        .all()
    )

    orders_by_status = [
        {
            "status" : status, 
            "order_count" : order_count or 0
        }
        for status, order_count in results
    ]

    return {
        "orders_by_status" : orders_by_status
    }

def get_sales_by_date_range(
        db : Session, 
        start_date : datetime, 
        end_date : datetime
):

    quantity = (
        db.query(
            func.sum(OrderItem.quantity)
        )
        .join(
            Order, 
            Order.id == OrderItem.order_id
        )
        .filter(
            Order.created_at >= start_date, 
            Order.created_at <= end_date
        )
        .scalar()
    )

    return {
        "start_date" : start_date, 
        "end_date" : end_date, 
        "quantity" : quantity or 0
    }

def get_product_sales(
        db : Session
):

    results = (
        db.query(
            Product.name, 
            func.sum(OrderItem.quantity)
        )
        .join(
            OrderItem, 
            Product.id == OrderItem.order_id
        )
        .group_by(
            Product.id, 
            Product.name
        )
        .order_by(
            func.sum(OrderItem.quantity).desc()
        )
        .all()
    )

    product_sales = [
        {
            "product" : product, 
            "quantity_sold" : quantity_sold or 0
        }
        for product, quantity_sold in results
    ]

    return {
        "product_sales" : product_sales
    }