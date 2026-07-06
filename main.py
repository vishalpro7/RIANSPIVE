from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.products import router as product_router
from routers.orders import router as order_router
from routers.payments import router as payment_router
from routers.admin import router as admin_router
from routers.shipments import router as shipment_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(admin_router)
app.include_router(shipment_router)