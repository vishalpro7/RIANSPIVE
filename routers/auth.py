from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from auth.security import hash_password
from fastapi.security import OAuth2PasswordRequestForm


from database.db import SessionLocal
from models.user_model import User
from schemas.user_schema import UserCreate
from schemas.user_schema import UserResponse
from schemas.user_schema import (UserLogin, TokenResponse)
from auth.security import (verify_password, create_access_token)
from services.auth_service import get_current_user
from dependencies.roles import require_role
from schemas.product_schema import (ProductResponse,ProductCreate)

router = APIRouter(
    prefix = "/auth",
    tags = ["Authentication"]
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    
    finally:
        db.close()


@router.post("/register", response_model = UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        name = user.name,
        email = user.email,
        password = hash_password(user.password),
        role = user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get(
    "/users",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    return users

@router.get("/users/{user_id}", response_model = UserResponse)
def get_user(
    user_id : int, db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user: 
        raise HTTPException(
            status_code = 404,
            detail = "User Not Found!"
        )

    return user

@router.post(
    "/login",
    response_model = TokenResponse
)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
    User.email == form_data.username
).first()
    
    verify_password(
        form_data.password,
        user.password
    )

    if not verify_password(
        form_data.password,
        user.password
    ):
        raise HTTPException(
            status_code = 401,
            details = "Invalid Credentials"
        )

    token = create_access_token(
        {
            "sub" : user.email
        }
    )

    return {
    "access_token": token,
    "token_type": "bearer"
}


@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user=Depends(get_current_user)
):
    return current_user

@router.get("/admin")
def admin_only_route(
    current_user = Depends(require_role("Admin"))
):
    return {
        "message" : "Welcome Admin!",
        "user" : current_user.name
    }

