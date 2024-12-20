from typing import List

import fastapi
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from pydantic_schemas.course import CourseCreate, Course, CourseBase
from db.db_setup import get_db

from api.utils.courses import get_course, get_courses, create_course,update_course, delete_course

router = fastapi.APIRouter()


@router.get("/courses", response_model=List[Course])
async def read_courses(db: Session = Depends(get_db)):
     courses = get_courses(db=db)
     return courses

@router.post("/courses", response_model=Course)
async def create_new_course(course: CourseCreate, db: Session = Depends(get_db)):
    return create_course(db=db, course=course)

@router.get("/courses/{course_id}")
async def read_course(course_id: int, db: Session = Depends(get_db)):
    db_course = get_course(db=db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail='Cousre not found.')
    return db_course

@router.patch("/courses/{course_id}", response_model=Course)
async def update_course_api(course_id: int, course_update: CourseBase, db: Session = Depends(get_db)):
    updated_course = update_course(db=db, course_id=course_id, course_update=course_update)
    if not updated_course:
        raise HTTPException(status_code=404, detail="Course not found.")
    return updated_course

@router.delete("/courses/{course_id}", status_code=204)
async def delete_course_api(course_id: int, db: Session = Depends(get_db)):
    deleted_course = delete_course(db=db, course_id=course_id)
    if not deleted_course:
        raise HTTPException(status_code=404, detail="Course not found.")
    return {"message": "Course deleted successfully"}

@router.get("/courses/{course_id}/sections")
async def read_course_sections():
    return {"courses": []}