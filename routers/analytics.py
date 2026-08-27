from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import SessionLocal
from datetime import datetime, timedelta

from database.db import get_db
from services.analytics_service import (
    get_analytics, 
    get_revenue_analytics, 
    get_time_based_revenue, 
    get_date_based_analytics, 
    get_revenue_by_status
)
from services.auth_service import get_current_user

router = APIRouter(
    prefix = "/analytics", 
    tags = ["Analytics"]
)

@router.get("/")
def analytics(
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_analytics(db)


@router.get("/revenue")
def revenue_analytics(
    db : Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    return get_revenue_analytics(db)


@router.get("/revenue/range")
def revenue_by_date_range(
        start_date: datetime,
        end_date: datetime,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    
    return get_date_based_analytics(
        db=db,
        start_date=start_date,
        end_date=end_date
    )


@router.get("/time-based")
def time_based(
    db : Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    return get_time_based_revenue(db)

@router.get("/status")
def revenue_by_status(
    db : Session = Depends(get_db)
):
    return get_revenue_by_status(db)

