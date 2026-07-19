from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Task, User
from schemas import TaskCreate, TaskResponse, UserResponse
from security import get_current_user_email

router = APIRouter(tags=["Tasks"])

@router.get("/users/me", response_model=UserResponse)
def read_users_me(current_user_email: str = Depends(get_current_user_email), db: Session = Depends(get_db)):
    current_user = db.query(User).filter(User.email == current_user_email).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return current_user

@router.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, current_user_email: str = Depends(get_current_user_email), db: Session = Depends(get_db)):
    current_user = db.query(User).filter(User.email == current_user_email).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    new_task = Task(title=task.title, description=task.description, owner_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@router.get("/tasks", response_model=list[TaskResponse])
def list_tasks(current_user_email: str = Depends(get_current_user_email), db: Session = Depends(get_db)):
    current_user = db.query(User).filter(User.email == current_user_email).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    tasks = db.query(Task).filter(Task.owner_id == current_user.id).all()
    return tasks

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskCreate, current_user_email: str = Depends(get_current_user_email), db: Session = Depends(get_db)):
    current_user = db.query(User).filter(User.email == current_user_email).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    existing_task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    existing_task.title = task.title
    existing_task.description = task.description
    db.commit()
    db.refresh(existing_task)

    return existing_task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, current_user_email: str = Depends(get_current_user_email), db: Session = Depends(get_db)):
    current_user = db.query(User).filter(User.email == current_user_email).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    db.delete(task)
    db.commit()

    return {"message": "Tarefa deletada com sucesso"}