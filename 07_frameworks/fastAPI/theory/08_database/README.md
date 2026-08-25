# Topic: Database with SQLAlchemy

Every previous topic used a plain Python list as a fake "database" --
data that disappears every time you restart the server. This topic
replaces that with a REAL database: SQLite (a file-based database,
zero setup required) via SQLAlchemy, the most widely used ORM in the
Python ecosystem.

Coming from Spring Boot, think of it this way:
- SQLAlchemy Engine       -> like the DataSource configured from
                              application.properties
- SQLAlchemy Session      -> like an EntityManager / Hibernate Session
- declarative Base model  -> like a class annotated with @Entity
- Depends(get_db)         -> like Spring injecting a Session per
                              request (open-session-in-view pattern),
                              except here it's explicit and per-endpoint
- db.query(Model)...      -> like using JPQL/Criteria API, but with a
                              more Pythonic, chainable syntax

Why SQLite for learning: it requires NO server, NO installation, NO
credentials -- the "database" is just a single file
(`app.db`) created automatically the first time you run the app.
Everything you learn here (sessions, models, queries) transfers
directly to PostgreSQL later -- you'd only change ONE line (the
connection string in `database.py`).

## Install the new dependency

    pip install sqlalchemy

## This folder's structure

    theory/08_database/
    ├── database.py   # engine, SessionLocal, Base, get_db dependency
    ├── models.py     # SQLAlchemy ORM models (the "@Entity" classes)
    ├── schemas.py    # Pydantic models for request/response (from topic 4/5)
    └── main.py       # FastAPI app using everything together

## How to run this example

From INSIDE `theory/08_database/`:

    uvicorn main:app --reload

This creates a file `app.db` in that same folder the first time you
run it (or the first time a table is needed). You can delete `app.db`
any time to reset all data -- it will be recreated automatically.

## Key takeaways

1. `database.py` centralizes the connection setup: the `engine` (talks
   to the actual database file), `SessionLocal` (a factory that
   creates new sessions), and `Base` (the parent class every ORM
   model inherits from).
2. A model in `models.py` (e.g. `class Book(Base):`) maps directly to
   a database table -- each class attribute becomes a column, exactly
   like `@Column` fields on a JPA `@Entity`.
3. `get_db()` is a dependency (from topic 6!) that opens a session,
   `yield`s it to the endpoint, and guarantees it's closed afterward
   -- even if the endpoint raises an exception. This `yield`-based
   dependency pattern is specific to resources that need cleanup
   (sessions, file handles, connections).
4. Notice models.py (SQLAlchemy) and schemas.py (Pydantic) are
   DIFFERENT things, on purpose -- the ORM model represents the
   database table, the Pydantic schema represents the API's input/
   output shape. This mirrors the Input/Output model separation from
   topic 5 (response_model), just one layer deeper.
5. `db.add(obj)` + `db.commit()` + `db.refresh(obj)` is the standard
   "create" sequence: stage the change, save it, then reload the
   object so it has the database-generated fields (like the auto
   `id`).
