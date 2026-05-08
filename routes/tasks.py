from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from core.security import get_current_user
import models.user as user_model
import models.task as task_model
import schemas.task as task_schema

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

# ─── CREATE TASK ─────────────────────────────────

@router.post("/", response_model=task_schema.TaskResponse, status_code=201)
def create_task(
    task: task_schema.TaskCreate,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    """Create a new task — login required"""
    new_task = task_model.Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        owner_id=current_user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# ─── GET ALL MY TASKS ────────────────────────────

@router.get("/", response_model=list[task_schema.TaskResponse])
def get_all_tasks(
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    """Get all tasks for logged in user"""
    tasks = db.query(task_model.Task).filter(
        task_model.Task.owner_id == current_user.id
    ).all()
    return tasks

