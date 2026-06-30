from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship

from database.db import SessionLocal

from models.order_model import Order
from models.order_item_model import OrderItem
from models.product_model import Product

from schemas.order_schema import OrderCreate
from schemas.order_schema import OrderResponse
from services.auth_service import get_current_user
from schemas.order_schema import OrderSummary
from schemas.order_schema import OrderDetailResponse, OrderStatusUpdate
from services.order_service import create_order
from services import order_service



router = APIRouter(
    prefix = "/orders",
    tags = ["Orders"]
)

def get_db():

    db = SessionLocal()

    try: 
        yield db
    
    finally:

        db.close()


@router.post(
    "/",
    response_model = OrderResponse
)
def create_order(
    order : OrderCreate,
    current_user = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    return order_service.create_order(
        db = db, 

        order = order , 

        current_user = current_user
    )


@router.get(
    "/my-orders",
    response_model=list[OrderSummary]
    )
def get_my_orders(
    current_user = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    return order_service.get_my_orders(
        current_user = current_user, 
        db = db
    )


@router.get(
    "/{order_id}",
    response_model = OrderDetailResponse)
def get_order(
    order_id : int,
    current_user = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    
    return order_service.get_order(
        order_id = order_id, 
        current_user = current_user, 
        db = db
    )


@router.put(
    "/{order_id}", 
    response_model = OrderResponse
)
def update_order_status(
    order_id : int, 

    order_status : OrderStatusUpdate, 

    db : Session = Depends(get_db)
):
    
    return order_service.update_order_status(
        db = db, 

        order_id = order_id, 

        order_status = order_status
    )


@router.delete(
    "/{order_id}"
)
def delete_order(
    order_id : int, 
    db : Session = Depends(get_db)
):
    
    return order_service.delete_order(
        order_id = order_id, 
        db = db
    )