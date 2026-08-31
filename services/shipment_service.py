from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.shipment_model import Shipment
from models.order_model import Order

from schemas.shipment_schema import ShipmentCreate, ShipmentUpdate


ALLOWED_STATUS = {
    "PROCESSING",
    "PACKED",
    "SHIPPED",
    "OUT_FOR_DELIVERY",
    "DELIVERED",
    "RETURNED",
    "CANCELLED"
}


SHIPMENT_STATUS_TRANSITIONS = {
    "PROCESSING" : ["PACKED"], 
    "PACKED" : ["SHIPPED"], 
    "SHIPPED" : ["OUT FOR DELIVERY", "RETURNED"], 
    "OUT FOR DELIVERY" : ["DELIVERED", "RETURNED"], 
    "DELIVERED" : [], 
    "RETURNED" : [], 
    "CANCELLED" : []
}


SHIPMENT_ORDER_STATUS_MAP = {
    "PROCESSING" : "PROCESSING", 
    "PACKED" : "PROCESSING", 
    "SHIPPED" : "SHIPPED", 
    "OUT FOR DELIVERY" : "SHIPPED", 
    "DELIVERED" : "DELIVERED", 
    "RETURNED" : "CANCELLED"
}

def get_shipment_by_id(
        db : Session, 
        shipment_id : int
):
    
    shipment = (
        db.query(Shipment).filter(
            Shipment.id == shipment_id
        ).first()
    )

    if shipment is None:

        raise HTTPException(
            status_code = 404, 
            detail = "Shipment Not Found!"
        )
    
    return shipment


def create_shipment(
        db : Session, 
        shipment : ShipmentCreate
):
    
    order = (
        db.query(Order)
        .filter(
            Order.id == shipment.order_id
        )
        .first()
    )

    if order is None:

        raise HTTPException(
            status_code = 404,
            detail = "Order not found"
        )

    if order.status != "PROCESSING":
        raise HTTPException(
            status_code = 400, 
            detail = "Shipment can only be created when the order is in PROCESSING state"
        )
    
    
    existing = (
        db.query(Shipment)
        .filter(
            Shipment.order_id == shipment.order_id
        )
        .first()
    )

    if existing:

        raise HTTPException(
            status_code = 400, 
            detail = "Shipment already exists for this order!"
        )
    
    new_shipment = Shipment(
        order_id = shipment.order_id, 

        address = shipment.address, 

        courier = shipment.courier, 

        tracking_number = shipment.tracking_number
    )

    db.add(new_shipment)

    db.commit()

    db.refresh(new_shipment)

    return new_shipment

def get_shipment(
        db : Session, 
        shipment_id : int
):
    
    return get_shipment_by_id(
        db = db, 
        shipment_id = shipment_id
    )


def update_shipment(
        db : Session, 
        shipment_id : int, 
        shipment_update : ShipmentUpdate
):
    
    shipment = get_shipment_by_id(
        db = db, 
        shipment_id = shipment_id
    )

    if shipment_update.status not in SHIPMENT_STATUS_TRANSITIONS[shipment.status]:
        raise HTTPException(
            status_code = 400, 
            detail = f"Cannot Change shipment status from {shipment.status} to {shipment_update.status}"
        )
    
    shipment.status = shipment_update.status

    order = (
        db.query(Order)
        .filter(Order.id == shipment.order_id)
        .first()
    )

    if order:
        order.status = SHIPMENT_ORDER_STATUS_MAP[shipment_update.status]

    db.commit()

    db.refresh(shipment)

    return shipment

def delete_shipment(
        db : Session, 
        shipment_id : int
):
    
    shipment = get_shipment_by_id(
        db = db, 
        shipment_id = shipment_id
    )

    db.delete(shipment)

    db.commit()

    return {
        "message" : "Shipment Deleted successfully!"
    }



