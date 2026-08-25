# Exercise 3: One-to-many relationship + routers integration

## Goal
Combine topic 7 (routers) with topic 8 (database): a real one-to-many
relationship (one Author has many Books), split across two router
files that both import the same shared models/database/schemas.

This is the closest thing yet to how your PS1 Spring Boot project is
probably structured (Entity with a @OneToMany, split into separate
Controllers).

## Structure to build

    exercise_03/
    ├── database.py        (same generic file as previous exercises)
    ├── models.py
    ├── schemas.py
    ├── main.py
    └── routers/
        ├── __init__.py    (empty file, already created for you)
        ├── authors.py
        └── books.py

## Instructions

1. In `models.py`:
   - Define `class Author(Base):` with `__tablename__ = "authors"`
     - id (Integer, primary_key, index)
     - name (String, nullable=False)
     - country (String, nullable=False)
     - `books = relationship("Book", back_populates="author")`
       (this is the ORM-level link, similar to @OneToMany(mappedBy=...))
   - Define `class Book(Base):` with `__tablename__ = "books"`
     - id (Integer, primary_key, index)
     - title (String, nullable=False)
     - author_id = Column(Integer, ForeignKey("authors.id"))
       (similar to @ManyToOne + @JoinColumn)
     - `author = relationship("Author", back_populates="books")`

   You'll need these imports in models.py:
   `from sqlalchemy import Column, ForeignKey, Integer, String`
   `from sqlalchemy.orm import relationship`

2. In `schemas.py`:
   - `AuthorCreate` (input): name (str), country (str)
   - `BookCreate` (input): title (str), author_id (int)
   - `BookOut` (output): id (int), title (str), author_id (int),
     with `model_config = ConfigDict(from_attributes=True)`
   - `AuthorOut` (output): id (int), name (str), country (str),
     books (list[BookOut] = []),
     with `model_config = ConfigDict(from_attributes=True)`

     Notice AuthorOut nests BookOut -- when you return an Author ORM
     object, Pydantic will automatically walk `.books` (thanks to the
     `relationship()` in models.py) and serialize each one using
     BookOut. This is what makes "get an author with all their books
     in one response" possible with almost no extra code.

3. In `routers/authors.py`:
   - `router = APIRouter(prefix="/authors", tags=["authors"])`
   - `POST ""` (response_model=AuthorOut): create an author
   - `GET ""` (response_model=list[AuthorOut]): list all authors
     (each one will include its nested books automatically)
   - `GET "/{author_id}"` (response_model=AuthorOut): get one author,
     raise HTTPException(404, "Author not found") if missing

4. In `routers/books.py`:
   - `router = APIRouter(prefix="/books", tags=["books"])`
   - `POST ""` (response_model=BookOut): create a book.
     IMPORTANT: before creating it, check that the given `author_id`
     actually exists (`db.query(models.Author).filter(...).first()`);
     raise HTTPException(404, "Author not found") if it doesn't --
     this is how you enforce a foreign key relationship makes sense
     at the API level, not just at the database level.
   - `GET ""` (response_model=list[BookOut]): list all books

5. In `main.py`:
   - `Base.metadata.create_all(bind=engine)`
   - create the app
   - `from routers import authors, books`
   - `app.include_router(authors.router)`
   - `app.include_router(books.router)`

## Run it

From INSIDE the `exercise_03/` folder:

    uvicorn main:app --reload

## Test in http://127.0.0.1:8000/docs

    POST /authors
    Body: {"name": "Frank Herbert", "country": "USA"}
    -> creates author with id: 1, books: []

    POST /books
    Body: {"title": "Dune", "author_id": 1}
    -> creates the book

    POST /books
    Body: {"title": "Nonexistent", "author_id": 999}
    -> 404 Author not found

    GET /authors/1
    -> should now show "books": [{"id": 1, "title": "Dune", ...}]
