"""Add, list, edit and delete users (no PATCH endpoint)."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserInput, UserOutput

user_controller = APIRouter(prefix="/users", tags=["Users"])


def save_changes(db: Session):
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="This email already exists") from exc


@user_controller.get("/", response_model=list[UserOutput])
def get_users(db: Session = Depends(get_db)):
    return db.scalars(select(User).order_by(User.id)).all()


@user_controller.post("/", response_model=UserOutput, status_code=status.HTTP_201_CREATED)
def add_user(data: UserInput, db: Session = Depends(get_db)):
    user = User(**data.model_dump())
    db.add(user)
    save_changes(db)
    db.refresh(user)
    return user


@user_controller.put("/{user_id}", response_model=UserOutput)
def edit_user(user_id: int, data: UserInput, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = data.name
    user.email = data.email
    user.age = data.age
    save_changes(db)
    db.refresh(user)
    return user


@user_controller.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
