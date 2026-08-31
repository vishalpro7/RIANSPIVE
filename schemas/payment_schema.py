from pydantic import BaseModel

class PaymentCreate(BaseModel):

    order_id : int


class PaymentUpdate(BaseModel):

    payment_id : int
    status : str

class PaymentResponse(BaseModel):

    id : int
    
    order_id : int

    amount : int

    status : str


    class Config:

        from_attributes = True