from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database.db import SessionLocal

from models.user_model import User
from models.product_model import Product
from models.order_model import Order
from models.payment_model import Payment

from services.auth_service import get_current_user
from services import dashboard_services
from schemas.dashboard_schema import DashBoardResponse
from schemas.analytics_schema import AnalyticsResponse
from services import analytics_service


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def admin_only(current_user):

    if current_user.role != "Admin":

        raise HTTPException(
            status_code=403,
            detail="Access Denied"
        )

    return current_user


@router.get("/users")
def get_all_users(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    admin_only(current_user)

    users = db.query(User).all()

    return users


@router.get("/orders")
def get_all_orders(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    admin_only(current_user)

    orders = db.query(Order).all()

    return orders


@router.get("/payments")
def get_all_payments(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    admin_only(current_user)

    payments = db.query(Payment).all()

    return payments


@router.get("/products")
def get_all_products(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    admin_only(current_user)

    products = db.query(Product).all()

    return products


@router.get("/stats")
def get_platform_stats(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    admin_only(current_user)

    total_users = db.query(User).count()

    total_products = db.query(Product).count()

    total_orders = db.query(Order).count()

    total_payments = db.query(Payment).count()

    return {
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_payments": total_payments
    }


@router.get(
    "/dashboard", 
    response_model = DashBoardResponse
)
def get_dashboard(
    db : Session = Depends(get_db)
):
    
    return dashboard_services.get_dashboard(db)


@router.get(
    "/analytics", 
    response_model = AnalyticsResponse
)
def get_analytics(
    db : Session = Depends(get_db)
):
    
    return analytics_service.get_analytics(db)