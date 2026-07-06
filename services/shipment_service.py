from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.shipment_model import Shipment
from models.order_model import Order

from schemas.shipment_schema import ShipmentCreate, ShipmentUpdate


ALLOWED_STATUS = {
    "Processing", 

    "Packed", 

    "Shipped", 

    "Out For Delivery", 

    "Delivered", 

    "Returned"
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
            status_code = "404",
            detail = "Order not found"
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

    if shipment_update.status not in ALLOWED_STATUS:

        raise HTTPException(
            status_code = 400, 
            detail = "Invalid Shipment Status!"
        )
    
    shipment.status = shipment_update.status

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



