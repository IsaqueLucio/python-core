# Topic: Configuration, Middlewares & Deploy

This is the final topic -- it closes the loop on things left
intentionally unfinished earlier: the hardcoded SECRET_KEY from topic
9, no CORS handling, no logging, and no way to actually ship any of
this anywhere. This topic fixes all of that.

Coming from Spring Boot, think of it this way:
- pydantic-settings + .env    -> like application.properties /
                                   application.yml, reading values
                                   from the environment instead of
                                   hardcoding them
- CORSMiddleware               -> same CORS concept you'd configure
                                   via @CrossOrigin or a
                                   WebMvcConfigurer bean
- @app.middleware("http")      -> like a Spring Filter or
                                   HandlerInterceptor -- code that
                                   runs on EVERY request, before/after
                                   your endpoint
- Dockerfile                   -> same idea as a Spring Boot fat JAR +
                                   Dockerfile, just with a different
                                   base image and entrypoint

## Install the new dependency

    pip install "pydantic-settings"

## This folder's structure

    theory/12_config_deploy/
    ├── .env.example     # template showing WHICH variables are needed
    ├── config.py         # Settings class, reads from .env
    ├── main.py            # app using Settings + CORS + logging middleware
    ├── requirements.txt    # formalized dependency list (finally!)
    ├── Dockerfile           # containerizes the app
    └── .dockerignore

## Part 1: environment variables with pydantic-settings

NEVER hardcode secrets (database URLs, JWT secret keys, API keys) in
your code -- especially not in code that gets committed to Git. The
fix: a `.env` file (NEVER committed -- always in `.gitignore`) holding
the real values, and a `Settings` class that reads them:

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    algorithm: str = "HS256"          # has a default -- optional
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
```

Then anywhere you'd have hardcoded `SECRET_KEY = "..."` (topic 9!),
you now do `from config import settings` and use `settings.secret_key`
instead. The actual value lives in `.env`, which is different on your
machine, a teammate's machine, and in production -- and is NEVER
visible in the code itself.

## Part 2: CORS (Cross-Origin Resource Sharing)

If a frontend running on `http://localhost:3000` tries to call your
API on `http://localhost:8000`, the BROWSER blocks it by default --
different origin (port), even on the same machine. This is a browser
security feature, not a FastAPI limitation. CORSMiddleware tells the
browser which origins are allowed to call your API:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your frontend's origin
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Part 3: custom middleware

A middleware runs for EVERY request, wrapping around the endpoint
call -- useful for logging, timing, or adding a header to every
response:

```python
import time

@app.middleware("http")
async def log_requests(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)   # this actually runs the endpoint
    elapsed = time.perf_counter() - start
    print(f"{request.method} {request.url.path} -> {elapsed:.3f}s")
    return response
```

Notice `call_next` is `await`ed -- middlewares are always async,
tying back to topic 10.

## Part 4: Dockerfile

A Dockerfile packages your app, its dependencies, and a specific
Python version into a portable image that runs the same way
everywhere -- your machine, a teammate's, a cloud server.

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

`--host 0.0.0.0` is important: `127.0.0.1` (what you've used all
along) only accepts connections from INSIDE the container -- `0.0.0.0`
accepts connections from outside it too, which is required for Docker
port mapping to work.

## How to run this example

    # locally, without Docker:
    cp .env.example .env    # then edit .env with real values
    uvicorn main:app --reload

    # with Docker:
    docker build -t learning-fastapi .
    docker run -p 8000:8000 --env-file .env learning-fastapi

## Key takeaways

1. `.env` holds secrets and environment-specific config; it's NEVER
   committed to Git (`.gitignore` it). `.env.example` (WITHOUT real
   values) documents which variables are needed, and IS committed.
2. `pydantic-settings` gives you the same validation/type-safety
   benefits from topic 4, applied to configuration instead of request
   bodies.
3. CORS errors happen in the BROWSER, not in your API -- if you test
   with Swagger/curl/Postman and it works, but a real frontend gets a
   CORS error, that's expected until CORSMiddleware is configured.
4. Middlewares run on every single request -- keep them fast, and
   remember `call_next` must be awaited.
5. `requirements.txt` (generated with `pip freeze > requirements.txt`,
   or curated by hand) is what makes your project reproducible on any
   machine, including inside Docker.
