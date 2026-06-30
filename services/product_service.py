from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from fastapi import HTTPException

from models.product_model import Product
from schemas.product_schema import ProductCreate

def create_product(
    product : ProductCreate,
    db : Session
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


def update_product(
    db : Session, 
    product_id : int, 
    product: ProductCreate
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


def delete_product(
    product_id : int,
    db : Session
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


def get_products(
        db : Session, 
        skip : int, 
        limit : int, 
        search : str | None, 
        min_price : int | None, 
        max_price : int | None, 
        sort_by : str, 
        order : str
):
    
    query = db.query(Product)

    if search :

        query = query.filter(
            Product.name.ilike(f"%{search}%")
        )

    if min_price is not None:

        query = query.filter(
            Product.price >= min_price
        )

    if max_price is not None:

        query = query.filter(
            Product.price <= max_price
        )

    allowed_columns = {
        "id" : Product.id , 
        "name" : Product.name, 
        "price" : Product.price, 
        "stock" : Product.stock
    }

    if sort_by not in allowed_columns:

        raise HTTPException(
            status_code = 400, 
            detail = "Invalid sort column"
        )
    
    sort_column = allowed_columns[sort_by]

    if order.lower() == "desc":

        query = query.order_by(
            desc(sort_column)
        )

    else : 

        query = query.order_by(
            asc(sort_column)
        )
    

    return query.offset(skip).limit(limit).all()


def get_product(
    db : Session, 
    product_id : int
):
    
    product = (
        db.query(Product).filter(
            Product.id == product_id
        ).first()
    )

    if product is None:

        raise HTTPException(
            status_code = 404, 
            detail = "Product not found!"
        )
    
    return product