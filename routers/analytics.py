from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import SessionLocal

from database.db import get_db
from services.analytics_service import get_analytics, get_revenue_analytics, get_time_based_revenue
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


@router.get("/revenue/time-based")
def time_based_revenue(
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_time_based_revenue(db)
