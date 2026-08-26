from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import SessionLocal

from database.db import get_db
from services.analytics_service import get_analytics
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