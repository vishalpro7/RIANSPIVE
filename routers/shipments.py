from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from database.db import SessionLocal

from schemas.shipment_schema import ShipmentCreate
from schemas.shipment_schema import ShipmentUpdate
from schemas.shipment_schema import ShipmentResponse

from services import shipment_service

router = APIRouter(
    prefix = "/shipments", 
    tags = ["Shipments"]
)


def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()



@router.post(
    "/", 
    response_model = ShipmentResponse
)
def create_shipment(
    shipment : ShipmentCreate, 
    db : Session = Depends(get_db)
):
    
    return shipment_service.create_shipment(
        db = db, 
        shipment = shipment
    )


@router.get(
    "/{shipment_id}",
    response_model = ShipmentResponse 
)
def get_shipment_by_id(
    shipment_id : int, 
    db : Session = Depends(get_db)
):
    
    return shipment_service.get_shipment(
        db = db, 
        shipment_id = shipment_id
    )



@router.put(
    "/{shipment_id}", 
    response_model = ShipmentResponse
)
def update_shipment(
    shipment_id : int, 
    shipment_update : ShipmentUpdate,
    db : Session = Depends(get_db)
):
    
    return shipment_service.update_shipment(
        db = db, 
        shipment_id = shipment_id, 
        shipment_update = shipment_update
    )


@router.delete(
    "/{shipment_id}", 
)
def delete_shipment(
    shipment_id : int, 
    db : Session = Depends(get_db)
):
    
    return shipment_service.delete_shipment(
        db = db,
        shipment_id = shipment_id
    )