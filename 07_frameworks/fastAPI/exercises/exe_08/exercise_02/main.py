"""
See INSTRUCTIONS.md for the full task description.
"""

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db
from schemas import TaskCreate, TaskOut, TaskUpdate

# TODO: create all tables
Base.metadata.create_all(bind=engine)

# TODO: create the FastAPI app instance
app = FastAPI()

# TODO: POST "/tasks" endpoint, response_model=TaskOut
@app.post("/tasks", response_model=TaskOut)
def post_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Tasks(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# TODO: GET "/tasks" endpoint, response_model=list[TaskOut]
# optional query param: done (bool | None = None)
# filter with db.query(models.Task).filter(models.Task.done == done).all()
# when done is provided, otherwise return all tasks
@app.get("/tasks", response_model=list[TaskOut])
def get_tasks(done: bool | None = None, db: Session = Depends(get_db)):
    if done is not None:
        tasks = db.query(models.Tasks).filter(models.Tasks.done == done).all()
        return tasks
    return db.query(models.Tasks).all()

# TODO: DELETE "/tasks/{task_id}" endpoint
@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Tasks).filter(models.Tasks.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    return task

# TODO: PATCH "/tasks/{task_id}" endpoint, response_model=TaskOut
# find the task, raise 404 if missing, apply only sent fields via setattr,
# commit, refresh, return it
@app.patch("/tasks/{task_id}", response_model=TaskOut)
def patch_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(models.Tasks).filter(models.Tasks.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task

# TODO: DELETE "/tasks/{task_id}" endpoint
# find the task, raise 404 if missing, db.delete(task), db.commit(),
# return {"message": "Task deleted"}
@app.delete("/task/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Tasks).filter(models.Tasks.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}