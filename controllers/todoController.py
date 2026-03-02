from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import User
from services.todoService import (
    get_all_todos,
    get_todos_by_user,
    create_todo,
    get_todo_by_id,
    update_todo,
    delete_todo,
    check_todo_belongs_to_user
)
from schemas import TodoCreate

def get_todos_controller(current_user: User, db: Session):
    return get_todos_by_user(current_user.id, db)

def get_todo_controller(todo_id: str, current_user: User, db: Session):
    if not check_todo_belongs_to_user(todo_id, current_user.id, db):
        raise HTTPException(status_code=404, detail="Todo not found")
    return get_todo_by_id(todo_id, db)

def create_todo_controller(todo: TodoCreate, current_user: User, db: Session):
    return create_todo(todo, current_user.id, db)

def update_todo_controller(todo_id: str, todo: TodoCreate, current_user: User, db: Session):
    if not check_todo_belongs_to_user(todo_id, current_user.id, db):
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo = get_todo_by_id(todo_id, db)
    return update_todo(db_todo, todo, db)

def delete_todo_controller(todo_id: str, current_user: User, db: Session):
    if not check_todo_belongs_to_user(todo_id, current_user.id, db):
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo = get_todo_by_id(todo_id, db)
    return delete_todo(db_todo, db)
