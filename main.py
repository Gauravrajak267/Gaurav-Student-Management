from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import create_engine, String, Integer, select
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column,
    Session, sessionmaker
)
from sqlalchemy.exc import IntegrityError

DATABASE_URL = "sqlite:///./students.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(
        String(254), unique=True
    )
    age: Mapped[int] = mapped_column(Integer)
    course: Mapped[str] = mapped_column(String(100))


class StudentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=254)
    age: int = Field(ge=1, le=120)
    course: str = Field(min_length=1, max_length=100)


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: str | None = Field(default=None, min_length=3, max_length=254)
    age: int | None = Field(default=None, ge=1, le=120)
    course: str | None = Field(default=None, min_length=1, max_length=100)


class StudentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    age: int
    course: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(

    title="Student Record Management API",
    lifespan=lifespan
)

app.mount(
    "/frontend",
    StaticFiles(directory="static", html=True),
    name="frontend"
)


def get_db():
    with SessionLocal() as db:
        yield db


@app.get("/")
def home():
    return {"message": "Student Management API is running"}


@app.post(
    "/students",
    response_model=StudentOut,
    status_code=status.HTTP_201_CREATED
)
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    values = data.model_dump()
    values["name"] = values["name"].strip()
    values["email"] = values["email"].strip().lower()
    values["course"] = values["course"].strip()

    if not all(values[k] for k in ("name", "email", "course")):
        raise HTTPException(422, "Fields cannot be blank")

    student = Student(**values)
    db.add(student)

    try:
        db.commit()
        db.refresh(student)
        return student
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Email already exists")


@app.get("/students", response_model=list[StudentOut])
def get_students(db: Session = Depends(get_db)):
    return db.scalars(select(Student).order_by(Student.id)).all()


@app.get("/students/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(404, "Student not found")
    return student


@app.patch("/students/{student_id}", response_model=StudentOut)
def update_student(
    student_id: int,
    data: StudentUpdate,
    db: Session = Depends(get_db)
):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(404, "Student not found")

    changes = data.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(400, "Provide fields to update")

    for key, value in changes.items():
        if value is None:
            raise HTTPException(422, f"{key} cannot be null")
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise HTTPException(422, f"{key} cannot be blank")
        if key == "email":
            value = value.lower()
        setattr(student, key, value)

    try:
        db.commit()
        db.refresh(student)
        return student
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Email already exists")


@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(404, "Student not found")

    db.delete(student)
    db.commit()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)