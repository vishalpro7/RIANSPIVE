from fastapi import APIRouter
from fastapi import Depends

from fastapi import Query

from services import product_service

from sqlalchemy.orm import Session

from database.db import SessionLocal



from schemas.product_schema import ProductCreate
from schemas.product_schema import ProductResponse

from typing import Optional

router = APIRouter(
    prefix = "/products",
    tags = ["Products"]
)

def get_db():

    db = SessionLocal()

    try : 
        
        yield db

    finally: 
        db.close()

@router.post("/",response_model = ProductResponse)
def create_product(
    product : ProductCreate,
    db : Session = Depends(get_db)
):
    return product_service.create_product(
        db = db, 
        product = product
    )

@router.get("/", response_model = list[ProductResponse])
def get_products(
    skip: int = Query(default=0, ge=0),

    limit: int = Query(default=10, ge=1, le=100),

    search: str | None = None,

    min_price: int | None = None,

    max_price: int | None = None,

    sort_by: str = "id",

    order: str = "asc",

    db: Session = Depends(get_db)
):
    
   return product_service.get_products(
       db = db, 

       skip = skip, 

       limit = limit, 

       search = search , 

       min_price = min_price, 

       max_price = max_price, 

       sort_by = sort_by, 

       order = order
   )


@router.get("/{product_id}", response_model = ProductResponse)
def get_product(
    product_id : int,
    db : Session = Depends(get_db)
):
    return product_service.get_product(
        db = db, 

        product_id = product_id
    )

@router.put(
    "/{product_id}",
    response_model = ProductResponse
)
def update_product(
    product_id : int,
    product : ProductCreate,
    db : Session = Depends(get_db)
):
    
    return product_service.update_product(
        db = db, 
        product_id = product_id, 
        product = product
    )


@router.delete("/{product_id}")
def delete_product(
    product_id : int,
    db : Session = Depends(get_db)
):
    
    return product_service.delete_product(
        product_id = product_id, 
        db = db
    )
