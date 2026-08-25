# Exercise 2: Full CRUD (Update + Delete) + filtering

## Goal
Complete the CRUD cycle: add UPDATE and DELETE, and practice a
database query with a WHERE-style filter (a query param).

## Structure to build

    exercise_02/
    ├── database.py   (same generic file as exercise_01, copy it)
    ├── models.py
    ├── schemas.py
    └── main.py

## Instructions

1. In `models.py`:
   - Define `class Task(Base):` with `__tablename__ = "tasks"`
   - Columns: id (Integer, primary_key, index), title (String,
     nullable=False), done (Boolean, default=False)

2. In `schemas.py`:
   - `TaskCreate` (input): title (str), done (bool = False)
   - `TaskUpdate` (input, for partial updates): title (str | None = None),
     done (bool | None = None)
   - `TaskOut` (output): id (int), title (str), done (bool),
     with `model_config = ConfigDict(from_attributes=True)`

3. In `main.py`:
   - `Base.metadata.create_all(bind=engine)` + create the app
   - `POST "/tasks"` (response_model=TaskOut): create a task
   - `GET "/tasks"` (response_model=list[TaskOut]) with an OPTIONAL
     query param `done: bool | None = None`:
       - if `done` is None, return all tasks
       - otherwise, filter: `db.query(models.Task).filter(models.Task.done == done).all()`
   - `PATCH "/tasks/{task_id}"` (response_model=TaskOut): receives a
     TaskUpdate, finds the task (raise 404 if missing), applies only
     the fields that were actually sent
     (`update.model_dump(exclude_unset=True)`), commits, refreshes,
     returns it.

     Hint for applying a partial update to an ORM object (different
     from the plain-dict pattern in topic 4 -- here you set attributes
     one by one):
     ```python
     for field, value in update.model_dump(exclude_unset=True).items():
         setattr(task, field, value)
     db.commit()
     db.refresh(task)
     ```
   - `DELETE "/tasks/{task_id}"`: finds the task (raise 404 if
     missing), calls `db.delete(task)`, `db.commit()`, and returns
     `{"message": "Task deleted"}`.

## Run it

From INSIDE the `exercise_02/` folder:

    uvicorn main:app --reload

## Test in http://127.0.0.1:8000/docs

    POST /tasks
    Body: {"title": "Study SQLAlchemy"}
    -> creates it, done defaults to false

    GET /tasks?done=false
    -> only unfinished tasks

    PATCH /tasks/1
    Body: {"done": true}
    -> only "done" changes, "title" stays the same

    DELETE /tasks/1
    -> {"message": "Task deleted"}

    GET /tasks
    -> task 1 is gone
