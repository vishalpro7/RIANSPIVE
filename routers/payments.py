from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from database.db import SessionLocal
from schemas.payment_schema import PaymentResponse, PaymentCreate, PaymentUpdate
from models.order_model import Order
from schemas.order_schema import OrderStatusUpdate
from models.payment_model import Payment
from services.auth_service import get_current_user
from services.payment_service import create_payment, update_payment_service, get_all_payments, get_payment_by_id


router = APIRouter(
    prefix = "/payments",
    tags = ["Payments"]
)

def get_db():

    db = SessionLocal()

    try:

        yield db
    
    finally:

        db.close()


@router.post(
        "/", 
        response_model = PaymentResponse)
def do_create_payment(
    payment : PaymentCreate, 
    db : Session = Depends(get_db)
):

    return create_payment(
        db = db, 
        payment = payment
    )


@router.put("/status", response_model = PaymentResponse)
def update_payment_status(
    payment_update : PaymentUpdate,
    current_user = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    return update_payment_service(
        payment_update = payment_update, 
        current_user = current_user, 
        db = db
    )

@router.get("/getpayments")
def all_payments(
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user) 
):
    return get_all_payments(
        db = db, 
        current_user = current_user
    )

@router.get("/{payment_id}")
def payment_by_id(
    payment_id : int, 
    db : Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    return get_payment_by_id(
        payment_id = payment_id, 
        db = db, 
        current_user = current_user
    )





    