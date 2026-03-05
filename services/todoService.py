from sqlalchemy.orm import Session
from sqlalchemy import desc
from models import Todo
from schemas import TodoCreate
from datetime import datetime

def get_all_todos(db: Session):
    return db.query(Todo).all()

def get_todos_by_user(user_id: str, db: Session):
    return db.query(Todo).filter(Todo.user_id == user_id).order_by(desc(Todo.created_at)).all()

def get_todo_by_id(todo_id: str, db: Session):
    return db.query(Todo).filter(Todo.id == todo_id).first()

def create_todo(todo: TodoCreate, user_id: str, db: Session):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        priority=todo.priority,
        isCompleted=todo.isCompleted,
        task_time=todo.task_time,
        notification_enabled=todo.notification_enabled,
        user_id=user_id,
        completed_at=datetime.now() if todo.isCompleted else None
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db_todo: Todo, todo: TodoCreate, db: Session):
    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo.priority = todo.priority
    db_todo.task_time = todo.task_time
    db_todo.notification_enabled = todo.notification_enabled

    # Set completed_at when marking as completed
    if todo.isCompleted and not db_todo.isCompleted:
        db_todo.completed_at = datetime.now()
    elif not todo.isCompleted and db_todo.isCompleted:
        db_todo.completed_at = None

    db_todo.isCompleted = todo.isCompleted
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db_todo: Todo, db: Session):
    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted"}

def check_todo_belongs_to_user(todo_id: str, user_id: str, db: Session):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()
    return todo is not None
