from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import SessionLocal, engine, Base
from app.models import Student

Base.metadata.create_all(bind=engine)

app = FastAPI()


class StudentCreate(BaseModel):
    name: str
    reg_no: str
    department: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {
        "status": "ok",
        "db": "connected",
        "student": "2012338"
    }


@app.post("/students")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_student = Student(
        name=student.name,
        reg_no=student.reg_no,
        department=student.department
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


@app.get("/students/{reg_no}")
def get_student(reg_no: str, db: Session = Depends(get_db)):
    return db.query(Student).filter(Student.reg_no == reg_no).first()
