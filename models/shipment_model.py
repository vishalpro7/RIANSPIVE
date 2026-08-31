from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Shipment(Base):

    __tablename__ = "shipments"

    id = Column(
        Integer, 
        primary_key = True, 
        index = True
    )

    order_id = Column(
        Integer, 
        ForeignKey("orders.id"), 
        unique = True, 
        nullable = False
    )

    address = Column(
        String(500), 
        nullable = False
    )

    courier = Column(
        String(100), 
        nullable = False
    )

    tracking_number = Column(
        String(100), 
        unique = True, 
        nullable = False
    )

    status = Column(
        String(50),
        default = "PROCESSING"
    )

    order = relationship(
        "Order", 
        back_populates = "shipment"
    )