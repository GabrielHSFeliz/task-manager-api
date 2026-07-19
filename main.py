from fastapi import FastAPI
from routers import auth, tasks

app = FastAPI(title="Task Manager API")

app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/")
def read_root():
    return {"message": "Task Manager API rodando!"}