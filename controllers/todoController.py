from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError, OperationalError
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
import logging

logger = logging.getLogger(__name__)

def get_todos_controller(current_user: User, db: Session):
    try:
        return get_todos_by_user(current_user.id, db)
    except (ProgrammingError, OperationalError) as e:
        logger.error(f"Database error in get_todos: {e}")
        error_msg = str(e)
        if "notification_sent" in error_msg and "does not exist" in error_msg:
            raise HTTPException(
                status_code=503,
                detail="Database migration pending. Please try again in a moment."
            )
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in get_todos: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

def get_todo_controller(todo_id: str, current_user: User, db: Session):
    try:
        if not check_todo_belongs_to_user(todo_id, current_user.id, db):
            raise HTTPException(status_code=404, detail="Todo not found")
        return get_todo_by_id(todo_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_todo: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

def create_todo_controller(todo: TodoCreate, current_user: User, db: Session):
    try:
        return create_todo(todo, current_user.id, db)
    except Exception as e:
        logger.error(f"Error in create_todo: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create todo")

def update_todo_controller(todo_id: str, todo: TodoCreate, current_user: User, db: Session):
    try:
        if not check_todo_belongs_to_user(todo_id, current_user.id, db):
            raise HTTPException(status_code=404, detail="Todo not found")
        db_todo = get_todo_by_id(todo_id, db)
        return update_todo(db_todo, todo, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_todo: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to update todo")

def delete_todo_controller(todo_id: str, current_user: User, db: Session):
    try:
        if not check_todo_belongs_to_user(todo_id, current_user.id, db):
            raise HTTPException(status_code=404, detail="Todo not found")
        db_todo = get_todo_by_id(todo_id, db)
        return delete_todo(db_todo, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete_todo: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to delete todo")
