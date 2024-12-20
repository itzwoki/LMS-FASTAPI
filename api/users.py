from typing import Optional, List

import fastapi 
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from pydantic_schemas.user import UserCreate, User
from pydantic_schemas.course import Course
from db.db_setup import get_db
from api.utils.users import get_user, get_user_by_email, get_users, create_user
from api.utils.courses import get_user_courses

router = fastapi.APIRouter()





@router.get("/users", response_model=List[User])
async def read_users(skip: int =0, limit: int =100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.post("/create-user", response_model=User, status_code=201)
async def create_new_user(user : UserCreate, db: Session = Depends (get_db)):
    db_user = get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already Registered.")
    return create_user(db=db, user=user)

@router.get("/get-user/{user_id}", response_model=User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User Not Found.")
    return db_user

@router.get("/users/{user_id}/course", response_model=List[Course])
async def read_user_courses(user_id: int, db: Session = Depends(get_db)):
    courses = get_user_courses(user_id=user_id, db=db)
    return courses