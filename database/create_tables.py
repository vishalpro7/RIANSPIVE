from database.db import engine
from database.db import Base
from models.payment_model import Payment
from models.user_model import User
from models.product_model import Product
from models.order_model import Order
from models.order_item_model import OrderItem
from models.shipment_model import Shipment


Base.metadata.create_all(bind = engine)

