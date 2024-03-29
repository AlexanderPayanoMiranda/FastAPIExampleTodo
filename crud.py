import models, schemas
from sqlalchemy.orm import Session


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "---hash"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)

    db.add(db_user)
    db.commit()

    db.refresh(db_user)

    return db_user


def create_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    db_todo = models.Todo(**todo.dict(), author_id=user_id)

    db.add(db_todo)
    db.commit()

    db.refresh(db_todo)

    return db_todo


def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Todo).offset(skip).limit(limit).all()


def get_todos_for_user(user_id: int, db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Todo).filter(models.Todo.author_id == user_id).offset(skip).limit(limit).all()
