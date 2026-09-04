from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from database.db import Base


class User(Base):

    __tablename__ = "users"

    id = Column (Integer, primary_key = True, index = True)
    name = Column (String(100), nullable = False)
    email = Column (String(150), unique = True, nullable = False)
    password = Column (String(255), nullable = False)
    role = Column (String(50), nullable = False)
    
    orders = relationship(
        "Order",
        back_populates = "user"
    )

    status_changes = relationship(
            "OrderStatusHistory", 
            back_populates="user"
        )

    

