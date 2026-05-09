from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from database.database import get_db
import models.user as user_model
import schemas.token as token_schema
import schemas.user as user_schema
import core.security as security

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

#  REGISTER 

@router.post("/register", response_model=user_schema.UserResponse, status_code=201)
def register(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""

    # Check if username already exists
    existing_user = db.query(user_model.User).filter(
        user_model.User.username == user.username
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )

    # Check if email already exists
    existing_email = db.query(user_model.User).filter(
        user_model.User.email == user.email
    ).first()
    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Hash the password before saving
    hashed_password = security.hash_password(user.password)

    # Create new user
    new_user = user_model.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



# LOGIN 

@router.post("/login", response_model=token_schema.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login and get JWT token"""

    # Find user by username
    user = db.query(user_model.User).filter(
        user_model.User.username == form_data.username
    ).first()

    # Check user exists and password is correct
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT token
    access_token = security.create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# GET MY PROFILE 

@router.get("/me", response_model=user_schema.UserResponse)
def get_my_profile(current_user: user_model.User = Depends(security.get_current_user)):
    """Get currently logged in user's profile"""
    return current_user
