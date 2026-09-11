# FastAPI Capstone 1: DevTrack API

## Overview

Build **DevTrack**, a backend API for managing software projects and their
issues. Users must be able to create accounts, authenticate with JWT, create
projects, report issues, update their work, search records, and access data
according to ownership and role-based authorization rules.

This capstone must be implemented from scratch. Only this specification is
provided: there is no starter code, no partially implemented function, and no
predefined solution structure beyond the required architecture below.

The application has no frontend. Its complete manual workflow must be usable
through FastAPI's interactive documentation at:

    http://127.0.0.1:8000/docs

## Learning objective

Integrate all twelve FastAPI topics from this module in one coherent project:

1. FastAPI application and endpoints
2. Path and query parameters
3. HTTP errors and status codes
4. Request bodies and Pydantic validation
5. Response models
6. Dependency injection
7. APIRouter and modular organization
8. SQLAlchemy and relational data
9. Password hashing, OAuth2, JWT, and role-based authorization
10. Correct async I/O with `async def`, `await`, and `httpx.AsyncClient`
11. Automated tests with pytest, TestClient, fixtures, and dependency overrides
12. Environment configuration, CORS, middleware, requirements, and Docker

## Spring Boot mental map

| FastAPI project concept | Spring Boot equivalent |
| --- | --- |
| `FastAPI()` | `@SpringBootApplication` plus web configuration |
| `APIRouter` | `@RestController` grouped by domain |
| Pydantic input/output models | Request and response DTOs with Bean Validation |
| SQLAlchemy models | JPA entities |
| `Depends(get_db)` | Injecting a repository/session dependency |
| `Depends(get_current_user)` | Spring Security context/filter chain |
| `HTTPException` | `ResponseStatusException` or handled domain exception |
| pydantic-settings and `.env` | `application.properties` / `application.yml` |
| FastAPI middleware | Servlet filter or `HandlerInterceptor` |
| pytest and TestClient | JUnit and MockMvc/TestRestTemplate |
| Uvicorn and Docker | Embedded server packaged in a container |

## Required project structure

Build the following structure inside this capstone folder:

```text
capstone_01/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── auth.py
│   ├── dependencies.py
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       ├── users.py
│       ├── projects.py
│       ├── issues.py
│       ├── integrations.py
│       └── admin.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_projects.py
│   ├── test_issues.py
│   └── test_admin.py
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile
├── requirements.txt
└── INSTRUCTIONS.md
```

You may add small support modules if they make a responsibility clearer, but
do not collapse the entire application into `main.py`.

## Domain model

### User

Required database fields:

| Field | Type and rules |
| --- | --- |
| `id` | Integer primary key with index |
| `username` | String, required, unique, indexed |
| `email` | String, required, unique, indexed |
| `hashed_password` | String, required; never expose it in an API response |
| `role` | String, required, defaults to `user`; allowed values are `user` and `admin` |

Relationships:

- A user can own many projects.
- A user can report many issues.

### Project

Required database fields:

| Field | Type and rules |
| --- | --- |
| `id` | Integer primary key with index |
| `name` | String, required |
| `description` | String, optional |
| `owner_id` | Foreign key referencing `users.id`, required |

Relationships:

- A project belongs to one owner.
- A project can contain many issues.

### Issue

Required database fields:

| Field | Type and rules |
| --- | --- |
| `id` | Integer primary key with index |
| `title` | String, required |
| `description` | String, optional |
| `status` | String, defaults to `open` |,8,l., 
| `priority` | String, defaults to `medium` |
| `project_id` | Foreign key referencing `projects.id`, required |
| `reporter_id` | Foreign key referencing `users.id`, required |

Allowed issue values:

- `status`: `open`, `in_progress`, `closed`
- `priority`: `low`, `medium`, `high`

Use SQLAlchemy `relationship()` and matching `back_populates` values so the
three models form real bidirectional relationships.

## Pydantic schemas

Create separate schemas for input and output. Do not use ORM models directly
as request or response bodies.

At minimum, implement:

- `UserCreate`: username, email, password
- `UserOut`: id, username, email, role
- `Token`: access_token and token_type
- `ProjectCreate`: name and optional description
- `ProjectUpdate`: optional name and optional description
- `ProjectOut`: id, name, description, owner_id
- `IssueCreate`: title, optional description, status, and priority
- `IssueUpdate`: optional title, description, status, and priority
- `IssueOut`: id, title, description, status, priority, project_id, reporter_id
- `GitHubProfileOut`: login, name, public_repos, and html_url

Output schemas that receive SQLAlchemy objects must enable
`from_attributes=True`.

Add meaningful validation constraints. Examples include non-empty names,
reasonable string lengths, valid email format, a password with a minimum
length, and strict allowed values for issue status and priority. Invalid input
must be rejected automatically with status `422`.

## Configuration

Use `pydantic-settings` to load at least these values:

```dotenv
APP_NAME=DevTrack API
DATABASE_URL=sqlite:///./devtrack.db
SECRET_KEY=replace-with-a-long-random-value
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Requirements:

- Commit `.env.example` with placeholder values.
- Create `.env` locally, but never commit or package it.
- `SECRET_KEY` must not have a usable hardcoded fallback.
- `database.py` must use the configured `DATABASE_URL`.
- Generate a local secret with `openssl rand -hex 32`.
- Add `.env`, database files, caches, and virtual environments to
  `.gitignore`.

## Authentication and authorization

Implement the following complete flow:

1. A new account registers with username, email, and plain-text password.
2. The password is hashed before the user is saved.
3. New public registrations always receive the `user` role. The client must
   never be able to select `admin` during registration.
4. Login uses `OAuth2PasswordRequestForm`. The Swagger `username` field must
   receive the account's email.
5. A successful login returns a signed JWT access token with an expiration.
6. Protected routes read `Authorization: Bearer <token>` through
   `OAuth2PasswordBearer`.
7. `get_current_user` decodes the token, loads the current user from the
   database, and returns `401` for a missing, invalid, expired, or orphaned
   token.
8. `require_admin` depends on `get_current_user` and returns `403` when the
   authenticated user is not an administrator.

Do not place passwords, password hashes, secret keys, or other sensitive data
inside the JWT or an API response.

Because public registration cannot create administrators, promote a test
account directly in the local SQLite database or write a small local script to
change its role. Do not add an unprotected endpoint that grants admin access.

## Required endpoints

Organize endpoints with routers, prefixes, and tags so `/docs` clearly groups
the API by responsibility.

### System

| Method | Path | Authentication | Expected behavior |
| --- | --- | --- | --- |
| GET | `/` | Public | Return the API name and a short message |
| GET | `/health` | Public | Return `{"status": "ok"}` |

### Authentication and users

| Method | Path | Authentication | Expected behavior |
| --- | --- | --- | --- |
| POST | `/auth/register` | Public | Create an account and return `UserOut`; use `201` |
| POST | `/auth/login` | Public | Validate form credentials and return a bearer token |
| GET | `/users/me` | Bearer token | Return the authenticated user's public data |

Registration must return `409` when the username or email is already in use.
Invalid login credentials must return `401` with a generic message that does
not reveal whether the email exists.

### Projects

| Method | Path | Authentication | Expected behavior |
| --- | --- | --- | --- |
| POST | `/projects` | Bearer token | Create a project owned by the current user; use `201` |
| GET | `/projects` | Bearer token | List projects with pagination and optional name search |
| GET | `/projects/{project_id}` | Bearer token | Return one project |
| PATCH | `/projects/{project_id}` | Owner or admin | Partially update a project |
| DELETE | `/projects/{project_id}` | Owner or admin | Delete a project; use `204` |

The list endpoint must accept:

- `skip: int = 0`, with a minimum of zero
- `limit: int = 10`, constrained from 1 through 100
- `search: str | None = None`, matching project names

Place pagination parsing in a reusable dependency instead of duplicating it.
Return `404` when a project does not exist and `403` when it exists but the
current user cannot modify it.

Deleting a project must also remove its related issues, either through an
explicit delete strategy or a correctly configured SQLAlchemy cascade.

### Issues

| Method | Path | Authentication | Expected behavior |
| --- | --- | --- | --- |
| POST | `/projects/{project_id}/issues` | Bearer token | Report an issue in an existing project; use `201` |
| GET | `/projects/{project_id}/issues` | Bearer token | List that project's issues with filters |
| GET | `/issues/{issue_id}` | Bearer token | Return one issue |
| PATCH | `/issues/{issue_id}` | Reporter, project owner, or admin | Partially update an issue |
| DELETE | `/issues/{issue_id}` | Reporter, project owner, or admin | Delete an issue; use `204` |

The issue list endpoint must support optional `status` and `priority` query
filters plus the shared pagination dependency. Reject unsupported filter
values with validation rather than silently returning an empty list.

The authenticated user becomes the issue reporter automatically. A client
must not be allowed to choose another `reporter_id` in the request body.

### Administrator

| Method | Path | Authentication | Expected behavior |
| --- | --- | --- | --- |
| GET | `/admin/users` | Admin only | Return all users using `UserOut` |
| DELETE | `/admin/users/{user_id}` | Admin only | Delete a user, but reject deleting the current admin |

Apply the admin dependency at router level. A normal authenticated account
must receive `403`; an unauthenticated request must receive `401`.

### Async external integration

| Method | Path | Authentication | Expected behavior |
| --- | --- | --- | --- |
| GET | `/integrations/github/{username}` | Bearer token | Fetch and return a public GitHub profile |

This endpoint must:

- Be declared with `async def`.
- Use `httpx.AsyncClient`, not the synchronous `requests` library.
- Await the outbound GET request to `https://api.github.com/users/{username}`.
- Configure a reasonable timeout.
- Return only the fields defined by `GitHubProfileOut`.
- Return `404` when GitHub reports that the user does not exist.
- Convert a timeout, connection failure, or unexpected upstream response into
  `502 Bad Gateway` without exposing a Python traceback to the client.

Keep SQLAlchemy endpoints as regular `def` functions because this project uses
the synchronous SQLAlchemy session introduced in topic 8. Do not put blocking
database calls inside an `async def` endpoint.

## Middleware and CORS

Configure CORS for these development origins:

- `http://localhost:3000`
- `http://localhost:5173`

Create one HTTP middleware that measures every request with
`time.perf_counter()`. It must:

- Await `call_next(request)`.
- Log the method, path, returned status code, and elapsed time.
- Add the elapsed time to an `X-Process-Time` response header.
- Return the original response after adding the header.

## Application assembly

`app/main.py` must remain small. Its responsibilities are:

- Create database tables for this learning project.
- Instantiate FastAPI with title, description, and version metadata.
- Configure CORS.
- Register the timing middleware.
- Include every router.
- Define only the root and health endpoints.

Business-specific endpoints belong in their corresponding routers.

## Required automated tests

Use pytest and `TestClient`. Tests must never write to the development
`devtrack.db`.

In `tests/conftest.py`:

- Create a separate SQLite test database.
- Override `get_db` through `app.dependency_overrides`.
- Provide fixtures for the client, unique user data, and authenticated headers.
- Create a clean database state for every test or every test session with
  explicit cleanup.
- Clear dependency overrides after testing.

Cover at least these behaviors:

1. Health check succeeds.
2. Registration succeeds and never returns a password or hash.
3. Duplicate email or username returns `409`.
4. Invalid request data returns `422`.
5. Correct credentials return an access token.
6. Wrong credentials return `401`.
7. `/users/me` rejects a missing token.
8. `/users/me` accepts a valid token.
9. An authenticated user can create a project.
10. Project pagination and search work.
11. A missing project returns `404`.
12. A different normal user cannot update another user's project.
13. An authenticated user can create and list issues.
14. Invalid issue status or priority returns `422`.
15. An unauthorized user cannot modify another user's issue.
16. Deleting a project removes its related issues.
17. A normal user receives `403` from the admin router.
18. An admin can list users.

Every test must be independent. A test may not rely on another test running
first or leaving records behind.

The external GitHub call may be verified manually through `/docs`; do not make
the core automated test suite depend on internet availability.

Run the suite from the capstone root:

    pytest -v

## Dependencies

Create a curated `requirements.txt` containing only packages actually required
to run or test this application. It must cover:

- FastAPI
- Uvicorn with standard extras
- SQLAlchemy
- pydantic-settings
- Email validation used by Pydantic
- Password hashing
- JWT encoding and decoding
- OAuth2 form parsing
- HTTPX
- pytest

Do not copy the entire output of a global Python environment into this file.

## Running locally

From the capstone root:

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env
    uvicorn app.main:app --reload

Then open:

    http://127.0.0.1:8000/docs

## Manual validation through `/docs`

Complete this sequence after implementing the project:

1. Call `GET /health`.
2. Register user A.
3. Try registering user A again and confirm `409`.
4. Log in as user A using the email in the form's `username` field.
5. Click **Authorize** and enter the bearer token when required by the Swagger
   UI authorization dialog.
6. Call `GET /users/me`.
7. Create a project and save its returned ID.
8. Create two issues with different statuses and priorities.
9. List the project's issues using status and priority filters.
10. Partially update one issue and confirm unspecified fields are preserved.
11. Look up a real GitHub account through the async integration.
12. Look up a nonexistent GitHub account and confirm the translated error.
13. Register and log in as user B.
14. Confirm user B receives `403` when changing user A's project.
15. Promote a test account to admin directly in the local database.
16. Confirm the admin can access `GET /admin/users`.
17. Delete the project and confirm its issues are no longer available.
18. Inspect a response outside Swagger with `curl -i` and confirm the
    `X-Process-Time` header is present.

## Docker

Create a Docker image using Python 3.12 slim. The Dockerfile must:

- Set a working directory.
- Copy and install `requirements.txt` before copying application source.
- Install dependencies without preserving pip's cache.
- Copy the project files.
- Expose port 8000.
- Start `uvicorn app.main:app` on host `0.0.0.0` and port 8000.

The `.dockerignore` must exclude virtual environments, Python caches, pytest
caches, `.env`, Git metadata, and SQLite database files.

Build and run from the capstone root:

    docker build -t devtrack-api .
    docker run --name devtrack-api \
      --env-file .env \
      -p 8000:8000 \
      devtrack-api

Verify the same `/docs` workflow against the container. The SQLite file lives
inside the container and disappears when that container is removed. Persistent
container data and migration tools are intentionally outside this capstone's
required scope.

## HTTP behavior checklist

Use status codes consistently:

| Status | Use in this project |
| --- | --- |
| `200 OK` | Successful reads, login, and updates |
| `201 Created` | Registration, project creation, and issue creation |
| `204 No Content` | Successful deletions; return no JSON body |
| `401 Unauthorized` | Missing or invalid authentication |
| `403 Forbidden` | Authenticated user lacks permission |
| `404 Not Found` | Requested resource does not exist |
| `409 Conflict` | Username or email already exists |
| `422 Unprocessable Entity` | Pydantic/query validation fails |
| `502 Bad Gateway` | External GitHub service cannot provide a valid response |

## Definition of done

The capstone is complete only when:

- All required routes appear under clear tags in `/docs`.
- The complete authentication flow works through Swagger UI.
- Request bodies and query parameters are validated.
- Response models prevent sensitive fields from leaking.
- Ownership and administrator permissions return the correct errors.
- All data is stored in related SQLAlchemy tables.
- The external HTTP call is truly asynchronous.
- The middleware runs on every request and adds its response header.
- All automated tests pass against an isolated database.
- No secret or local `.env` is tracked by Git.
- The Docker image builds and exposes a working `/docs` interface.
- You can explain why database routes use `def` while the HTTPX integration
  uses `async def`.

## Scope boundaries

Do not add a frontend to this capstone. The second capstone will introduce a
basic functional frontend and browser-to-API integration. Also leave database
migrations, refresh tokens, email confirmation, password reset, cloud deploy,
and PostgreSQL as future improvements; they are valuable, but they would hide
the concepts this project is intended to consolidate.
