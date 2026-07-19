from fastapi import FastAPI, Depends, HTTPException

from fastapi import FastAPI
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Task, User
from schemas import UserCreate, UserResponse, UserLogin, TaskCreate, TaskResponse
from security import hash_password, verify_password, create_access_token, get_current_user_email
app = FastAPI(title="Task Manager API")

@app.get("/")
def read_root():
    return {"message": "Task Manager API rodando!"}

@app.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Verifica se o usuário já existe
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já registrado")

    # Cria um novo usuário
    hashed_password = hash_password(user.password)
    new_user = User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Verifica se o usuário existe
    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user:
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")

    # Verifica a senha
    if not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")

    # Cria o token de acesso
    access_token = create_access_token(data={"sub": existing_user.email})

    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserResponse)
def read_users_me(current_user_email: str = Depends(get_current_user_email), db: Session = Depends(get_db)):
    # Obtém o usuário atual com base no email do token
    current_user = db.query(User).filter(User.email == current_user_email).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return current_user

@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, current_user_email: str = Depends(get_current_user_email), db: Session = Depends(get_db)):
    # Obtém o usuário atual com base no email do token
    current_user = db.query(User).filter(User.email == current_user_email).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Cria uma nova tarefa associada ao usuário atual
    new_task = Task(title=task.title, description=task.description, owner_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task