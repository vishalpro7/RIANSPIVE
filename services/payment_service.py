from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.order_model import Order
from models.payment_model import Payment
from models.order_item_model import OrderItem
from models.product_model import Product
from schemas.payment_schema import PaymentUpdate, PaymentCreate


PAYMENT_STATUS_TRANSITIONS = {
    "PENDING" : ["SUCCESS", "FAILED"], 
    "SUCCESS" : [],
    "FAILED" : []
}



def create_payment(
        db : Session, 
        payment : PaymentCreate, 
        current_user
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

    if order.user_id != current_user.id:
         raise HTTPException(
              status_code = 403, 
              detail = "You are not authorized to pay for this order"
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

    if payment_update.status == "SUCCESS":
         order = (
              db.query(Order)
              .filter(Order.id == payment.order_id)
              .first()
         )

         if order and order.status == "PENDING":
              order.status = "PROCESSING"

    elif payment_update.status == "FAILED":

        order = (
        db.query(Order)
        .filter(Order.id == payment.order_id)
        .first()
    )

        if order and order.status == "PENDING":

            order_items = (
            db.query(OrderItem)
            .filter(OrderItem.order_id == order.id)
            .all()
        )

            for item in order_items:

                product = (
                db.query(Product)
                .filter(Product.id == item.product_id)
                .first()
            )

                if product:
                    product.stock += item.quantity

            order.status = "CANCELLED"

    db.commit()

    db.refresh(payment)

    return payment

def get_all_payments(
          db : Session, 
          current_user
):

    if current_user.role != "Admin":
        raise HTTPException(
            status_code = 403, 
            detail = "Not Authorized!"
        )

    payments = (
          db.query(Payment)
          .all()
     )

    if not payments:
          raise HTTPException(
               status_code = 404, 
               detail = "No orders found!"
          )

    return payments;

def get_payment_by_id(
          payment_id : int, 
          db : Session, 
          current_user
):
    if current_user.role != "Admin":
        raise HTTPException(
             status_code = 403, 
             detail = "Not authorized"
        )

    payment = (
          db.query(Payment)
          .filter(Payment.id == payment_id)
          .first()
     )

    if not payment:
          raise HTTPException(
               status_code = 404, 
               detail = "Payment not found"
          )

    return payment
    
    
    