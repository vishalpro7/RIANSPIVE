from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from models.user_model import User
from models.product_model import Product
from models.order_model import Order
from models.payment_model import Payment
from services.dashboard_services import get_dashboard
from services.analytics_service import get_analytics



def admin_only(current_user):

    if current_user.role != "Admin" :
        raise HTTPException(
            status_code = 403, 
            detail = "You are not authorized to perform this action"
        )

    return current_user


def get_all_users(
        db : Session, 
        current_user
):
    admin_only(current_user)

    users = (
        db.query(User)
        .all()
    )

    return users

def get_all_orders(
        db : Session, 
        current_user
):
    admin_only(current_user)

    orders = (
        db.query(Order)
        .all()
    )

    return orders

def get_all_payments(
        db : Session, 
        current_user
):
    admin_only(current_user)

    payment = (
        db.query(Payment)
        .all()
    )

    return payment

def get_all_products(
        db : Session, 
        current_user
):
    admin_only(current_user)

    product = (
        db.query(Product)
        .all()
    )

    return product

def get_platform_stats(
        db : Session, 
        current_user
):
    admin_only(current_user)

    total_users = db.query(User).count()

    total_payments = db.query(Payment).count()

    total_orders = db.query(Order).count()

    total_products = db.query(Product).count()

    return {
        "total_users" : total_users, 
        "total_payments" : total_payments, 
        "total_orders" : total_orders, 
        "total_products" : total_products
    }


def get_dashboard_services(
        db : Session, 
        current_user
):
    return get_dashboard(
        db = db, 
        current_user = current_user
    )

def analytics(
        db : Session,
        current_user
):
    return get_analytics(
        db = db, 
        current_user = current_user
    )

