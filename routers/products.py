from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from sqlalchemy import asc , desc


from sqlalchemy.orm import Session

from database.db import SessionLocal

from models.product_model import Product

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
    new_product = Product(
        name = product.name,
        description = product.description,
        price = product.price,
        stock = product.stock
    )    

    db.add(new_product)
    
    db.commit()

    db.refresh(new_product)

    return new_product

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
    
    query = db.query(Product)


    if search : 

        query = query.filter(
            Product.name.ilike(f"%{search}")
        )

    
    if min_price is not None:

        query = query.filter(
            Product.price >= min_price
        )

    
    if max_price is not None:

        query = query.filter(
            Product.price <= max_price
        )

    sort_column = getattr(Product, sort_by , Product.id)

    if order.lower() == "desc":

        query = query.order_by(
            
            desc(sort_column)

        )

    else : 

        query = query.order_by(

            asc(sort_column)
        )

    products = query.offset(skip).limit(limit).all()

    return products


@router.get("/{product_id}", response_model = ProductResponse)
def get_product(
    product_id : int,
    db : Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:

        raise HTTPException(
            status_code = 404,
            detail = "Product not Found!"
        )
    
    return product

@router.put(
    "/{product_id}",
    response_model = ProductResponse
)
def update_product(
    product_id : int,
    product : ProductCreate,
    db : Session = Depends(get_db)
):
    
    existing_product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not existing_product:
        raise HTTPException(
            status_code = 404,
            detail = "Product Not Found!"
        )
    
    existing_product.name = product.name
    existing_product.description = product.description
    existing_product.price = product.price
    existing_product.stock = product.stock

    db.commit()

    db.refresh(existing_product)

    return existing_product


@router.delete("/{product_id}")
def delete_product(
    product_id : int,
    db : Session = Depends(get_db)
):
    
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:

        raise HTTPException(
            status_code = 404,
            detail = "Product Not Found!"
        )
    
    db.delete(product)

    db.commit()

    return {
        "message" : "Product deleted successfully!"
    }

