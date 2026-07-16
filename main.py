from fastapi import FastAPI

app = FastAPI(title="Task Manager API")

@app.get("/")
def read_root():
    return {"message": "Task Manager API rodando!"}