from pydantic import BaseModel

class ShipmentCreate(BaseModel):

    order_id : int
    address : str
    courier : str
    tracking_number : str

class ShipmentUpdate(BaseModel):

    status : str

class ShipmentResponse(BaseModel):

    id : int
    order_id : int
    address : str
    courier : str
    tracking_number : str
    status : str

    class Config:

        from_attributes = True