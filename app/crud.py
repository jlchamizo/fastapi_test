from sqlalchemy.orm import Session
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = schemas.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_api_call(db: Session, api_call: schemas.APICallCreate):
    db_api_call = models.APICall(**api_call.dict())
    db.add(db_api_call)
    db.commit()
    db.refresh(db_api_call)
    return db_api_call

def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(**task.dict(), user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session, user_id: int):
    return db.query(models.Task).filter(models.Task.user_id == user_id).all()

def get_task(db: Session, task_id: int, user_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == user_id).first()

def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate, user_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == user_id).first()
    if db_task:
        update_data = task_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int, user_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == user_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False