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
from services.admin_service import (
    admin_only, 
    get_analytics, 
    get_all_users, 
    get_all_orders, 
    get_all_payments, 
    get_all_products,
    get_platform_stats, 
    get_dashboard_services
)


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

@router.get("/users")
def all_users(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return get_all_users(
        db = db, 
        current_user = current_user
    )


@router.get("/orders")
def all_orders(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return get_all_orders(
        db = db, 
        current_user = current_user
    )


@router.get("/payments")
def all_payments(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return get_all_payments(
        db = db, 
        current_user = current_user
    )


@router.get("/products")
def all_products(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_all_products(
        db = db, 
        current_user = current_user
    )
    

@router.get("/stats")
def platform_stats(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

   return get_platform_stats(
       db = db, 
       current_user = current_user
   )

@router.get(
    "/dashboard", 
    response_model = DashBoardResponse
)
def dashboard(
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_dashboard_services(
        db = db, 
        current_user = current_user
    )


@router.get(
    "/analytics", 
    response_model = AnalyticsResponse
)
def analytics(
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_analytics(
        db = db, 
        current_user = current_user
    )