from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship
from database.db import Base
from sqlalchemy import DateTime
from sqlalchemy.sql import func

class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, 
                primary_key = True,
                index = True)
    
    user_id = Column(Integer, 
                     ForeignKey("users.id"))
    
    total_amount = Column(Integer,
                          nullable = False)
    
    status = Column(
        String(50),
        nullable = False, 
        default = "PENDING"
    )
    
    user = relationship(
        "User",
        back_populates = "orders"
    )

    order_items = relationship(
        "OrderItem",
        back_populates = "order"
    )

    payment = relationship(
        "Payment", 
        back_populates = "order", 
        uselist = False
    )

    shipment = relationship(
        "Shipment", 
        back_populates = "order", 
        uselist = False
    )

    created_at = Column(
        DateTime(timezone = True),
        server_default = func.now(), 
        nullable = False 
    )
    
    