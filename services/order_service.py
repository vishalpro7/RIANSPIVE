from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.order_model import Order
from models.order_item_model import OrderItem
from models.product_model import Product

from schemas.order_schema import OrderCreate, OrderStatusUpdate
from services.product_service import get_product_by_id


ALLOWED_STATUS = [
        "Pending", 
        "Processing", 
        "Shipped", 
        "Delivered", 
        "Cancelled"
    ]



def get_order_by_id(
        db : Session, 
        order_id : int
):
    
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if order is None:

        raise HTTPException(
            status_code = 404, 
            detail = "Order not Found!"
        )
    
    return order



def create_order(
    db : Session, 

    order : OrderCreate, 

    current_user 
):
    total_amount = 0

    for item in order.items:

        product = get_product_by_id(
            db = db, 
            product_id = item.product_id
        )
        
        if product.stock < item.quantity:
            raise HTTPException(
                status_code = 400, 
                detail = f"Insufficient stock for {product.name}"
            )
        
        total_amount += (
            product.price * item.quantity
        )

    
    new_order = Order(
        user_id = current_user.id,
        total_amount = total_amount
    )

    db.add(new_order)

    for item in order.items:

        product = get_product_by_id(
            db = db, 
            product_id = item.product_id
        )

        order_item = OrderItem(
            order_id = new_order.id, 

            product_id = item.product_id, 

            quantity = item.quantity
        )

        db.add(order_item)

        product.stock -= item.quantity

    db.commit()

    db.refresh(new_order)

    return new_order


def get_my_orders(
    current_user,
    db : Session 
):
    orders = db.query(Order).filter(
        Order.user_id == current_user.id
    ).all()

    return orders


def get_order(
    order_id : int,
    current_user ,
    db : Session 
):
    
    return get_order_by_id(
        db = db, 
        order_id = order_id
    )

def update_order_status(
        db : Session, 
        order_id : int, 
        order_status : OrderStatusUpdate
):
    
    order = get_order_by_id(
        db = db, 
        order_id = order_id
    )


    if order_status.status not in ALLOWED_STATUS:

        raise HTTPException(
            status_code = 400, 
            detail = "Invalid Order Status!"
        )
    
    order.status = order_status.status

    db.commit()

    db.refresh(order)

    return order

def delete_order(
        order_id : int, 
        db : Session
):
    
    order = get_order_by_id(
        db = db, 
        order_id = order_id
    )

    db.delete(order)

    db.commit()

    return {
        "message" : "order deleted successfully!"
    }