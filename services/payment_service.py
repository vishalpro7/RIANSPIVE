from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.order_model import Order
from models.payment_model import Payment
from schemas.payment_schema import PaymentUpdate, PaymentCreate


PAYMENT_STATUS_TRANSITIONS = {
    "PENDING" : ["SUCCESS", "FAILED"], 
    "SUCCESS" : [],
    "FAILED" : []
}



def create_payment(
        db : Session, 
        payment : PaymentCreate
):
    order = (
        db.query(Order)
        .filter(Order.id == payment.order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code = 404, 
            detail = "Order not found!"
        )

    existing_payment = (
        db.query(Payment)
        .filter(Payment.order_id == payment.order_id)
        .first()
    )

    if existing_payment:
        raise HTTPException(
            status_code = 400, 
            detail = "Payment Already exists"
        )

    new_payment = Payment(
        order_id = payment.order_id, 
        amount = order.total_amount, 
        status = "PENDING"
    )

    db.add(new_payment)

    db.commit()

    db.refresh(new_payment)

    return new_payment


def update_payment_service(
        payment_update :  PaymentUpdate,
        current_user,
        db : Session 
):
    if current_user.role != "Admin":
        raise HTTPException(
            status_code = 403, 
            details = "Access Denied!"
        )

    payment = (
        db.query(Payment)
        .filter(Payment.id == payment_update.payment_id)
        .first()
    )

    if not payment:
        raise HTTPException(
            status_code = 404, 
            detail = "Order not found!"
        )

    if payment_update.status not in PAYMENT_STATUS_TRANSITIONS[payment.status]:
            raise HTTPException(
                status_code = 400, 
                detail = f"Cannot Change payment from {payment.status} to {payment_update.status}"
            )

    payment.status = payment_update.status

    db.commit()

    db.refresh(payment)

    return payment
    
    
    