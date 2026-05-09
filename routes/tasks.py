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

# CREATE TASK 

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
        priority=task.priority,
        due_date=task.due_date,
        owner_id=current_user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# GET ALL MY TASKS 

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


#  GET SINGLE TASK 

@router.get("/{task_id}", response_model=task_schema.TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    """Get a single task by ID"""
    task = db.query(task_model.Task).filter(
        task_model.Task.id == task_id,
        task_model.Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# UPDATE TASK 

@router.put("/{task_id}", response_model=task_schema.TaskResponse)
def update_task(
    task_id: int,
    updated_task: task_schema.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    """Update a task by ID"""
    task = db.query(task_model.Task).filter(
        task_model.Task.id == task_id,
        task_model.Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Only update fields that were provided
    if updated_task.title is not None:
        task.title = updated_task.title
    if updated_task.description is not None:
        task.description = updated_task.description
    if updated_task.completed is not None:
        task.completed = updated_task.completed
    if updated_task.priority is not None:
        task.priority = updated_task.priority
    if updated_task.due_date is not None:
        task.due_date = updated_task.due_date

    db.commit()
    db.refresh(task)
    return task


# DELETE TASK 

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    """Delete a task by ID"""
    task = db.query(task_model.Task).filter(
        task_model.Task.id == task_id,
        task_model.Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"detail": "Task deleted successfully"}
