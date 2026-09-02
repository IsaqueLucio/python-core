# Exercise 3: Containerize a real API with Docker

## Goal
The capstone of this entire 12-topic module: take a real, working API
(reusing topic 8's database pattern) and package it into a Docker
image that runs anywhere -- proving the whole "works on my machine"
problem is solved.

## Structure to build

    exercise_03/
    ├── database.py    (same generic file from topic 8, copy it)
    ├── models.py
    ├── schemas.py
    ├── main.py
    ├── requirements.txt
    ├── Dockerfile
    └── .dockerignore

## Instructions

1. `database.py`: copy the generic version.

2. In `models.py`:
   - Define `class Book(Base):` with `__tablename__ = "books"`
   - Columns: id (Integer, primary_key, index), title (String,
     nullable=False), author (String, nullable=False)

3. In `schemas.py`:
   - `BookCreate` (input): title (str), author (str)
   - `BookOut` (output): id (int), title (str), author (str), with
     `model_config = ConfigDict(from_attributes=True)`

4. In `main.py`:
   - `Base.metadata.create_all(bind=engine)` + create the app
   - `POST "/books"` (response_model=BookOut): create a book
   - `GET "/books"` (response_model=list[BookOut]): list all books

5. Write `requirements.txt` with exactly what THIS project needs (not
   everything from every topic -- just fastapi, uvicorn[standard],
   sqlalchemy, since this exercise has no auth, no testing framework
   needed inside the image).

6. Write the `Dockerfile` -- same pattern as theory/12_config_deploy/Dockerfile
   (copy it, it's fully generic and doesn't need project-specific
   changes for this exercise).

7. Write `.dockerignore` -- same pattern as the theory file (exclude
   __pycache__, .pytest_cache, *.db, venv folders).

## Build and run it

From INSIDE the `exercise_03/` folder:

    docker build -t books-api .
    docker run -p 8000:8000 books-api

## Verify it actually works

While the container is running, from ANOTHER terminal:

    curl -X POST http://127.0.0.1:8000/books \
      -H "Content-Type: application/json" \
      -d '{"title": "Dune", "author": "Frank Herbert"}'

    curl http://127.0.0.1:8000/books

Both should work exactly like running with `uvicorn main:app --reload`
directly -- except now this is running INSIDE an isolated container,
with its own Python version and dependencies, completely independent
of what's installed on your actual machine. This is the same artifact
you'd hand off to a cloud platform (a VM, Kubernetes, a PaaS like
Render or Railway) to actually deploy it live.

## One thing to notice

The SQLite database created inside the container (`app.db`) lives
INSIDE that container's filesystem -- stop and remove the container,
and that data is gone. This is intentional for this exercise (keeps
things simple), but it's also why real deployments use an external
database (a managed PostgreSQL instance, for example) instead of a
SQLite file baked into the container -- something worth keeping in
mind as you move toward a real SaaS project.
