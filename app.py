from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def index():
    return {"Hello": "World"}


@app.get("/users", response_model=list[schemas.User])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip, limit)
    return users


@app.get("/user_by_id/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


@app.get("/user_by_email/{user_email}", response_model=schemas.User)
def get_user(user_email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user_email)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


@app.get("/users/{user_id}/todos", response_model=list[schemas.Todo])
def list_todos_for_user(user_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    user_todos = crud.get_todos_for_user(user_id, db, skip, limit)

    return user_todos


@app.post("/users/{user_id}/todos", response_model=schemas.Todo)
def create_todo(user_id: int, todo: schemas.TodoCreate, db: Session = Depends(get_db), ):
    todo = crud.create_todo(db, todo, user_id)

    return todo


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    check_email = crud.get_user_by_email(db, email=user.email)

    if check_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = crud.create_user(db, user)

    return db_user


@app.get("/todos", response_model=list[schemas.Todo])
def list_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip, limit)

    return todos
