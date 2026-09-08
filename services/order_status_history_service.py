from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.order_status_history_model import OrderStatusHistory
from models.order_model import Order

def create_status_history(
        db : Session, 
        order_id : int, 
        old_status : str, 
        new_status : str, 
        changed_by : int
):
    history = OrderStatusHistory(
        order_id = order_id, 
        old_status = old_status, 
        new_status = new_status, 
        changed_by = changed_by
    )

    db.add(history)

    return history

def get_order_status_history(
        db : Session, 
        order_id : int, 
        current_user
):

    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code = 404, 
            detail = "Order not found!"
        )

    if(current_user.role != "Admin" and order.user_id != current_user.id):
        raise HTTPException(
            status_code = 403, 
            detail = "Not authorized to access this order history"
        )
    
    history = (
        db.query(OrderStatusHistory)
        .filter(OrderStatusHistory.order_id == order_id)
        .order_by(OrderStatusHistory.changed_at)
        .all()
    )

    return history

