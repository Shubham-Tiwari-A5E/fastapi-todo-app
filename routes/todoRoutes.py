from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import TodoCreate, TodoResponse
from auth import get_current_user
from controllers.todoController import (
    get_todos_controller,
    get_todo_controller,
    create_todo_controller,
    update_todo_controller,
    delete_todo_controller
)

router = APIRouter()

@router.get("/todos", response_model=list[TodoResponse])
def get_todos(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_todos_controller(current_user, db)

@router.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_todo_controller(todo_id, current_user, db)

@router.post("/todos", response_model=TodoResponse)
def create_todo(todo: TodoCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_todo_controller(todo, current_user, db)

@router.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: str, todo: TodoCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return update_todo_controller(todo_id, todo, current_user, db)

@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return delete_todo_controller(todo_id, current_user, db)
