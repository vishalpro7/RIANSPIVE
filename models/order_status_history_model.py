from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship
from database.db import Base
from sqlalchemy import DateTime
from sqlalchemy.sql import func

class OrderStatusHistory(Base):

    __tablename__ = "order_status_history"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True
    )

    order_id = Column(
        Integer, 
        ForeignKey("orders.id"), 
        nullable = False
    )

    old_status = Column(
        String(50), 
        nullable = False
    )

    new_status = Column(
        String(50), 
        nullable = False
    )

    changed_by = Column(
        Integer, 
        ForeignKey("users.id"), 
        nullable = False
    )

    changed_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable = False
    )

    order = relationship(
        "Order", 
        back_populates="status_history"
    )

    user = relationship(
        "User", 
        back_populates="status_changes"
    )

    status_history = relationship(
        "OrderStatusHistory", 
        back_populates="order"
    )

    status_changes = relationship(
        "OrderStatusHistory", 
        back_populates="user"
    )
    