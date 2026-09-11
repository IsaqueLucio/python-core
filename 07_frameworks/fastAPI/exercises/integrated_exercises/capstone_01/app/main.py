from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import *
from app.database import Base, engine
import time

app = FastAPI(
    title="Learning FastAPI - Capstone 1: DevTrack API",
    description="A project and issue manager API.",
    version="0.1.0",
)

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["*"], 
    allow_headers=["*"]
)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(integrations.router)
app.include_router(issues.router)
app.include_router(projects.router)
app.include_router(users.router)

@app.middleware("http")
async def add_process_time_header(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start
    response.headers["X-Process-Time"] = str(elapsed)
    return response

@app.get("/")
def get():
    return {
        "api_name": "DevTrack API",
        "goal": "A project and issue manager API."
        }

@app.get("/health")
def get_health():
    return {"status": "ok"}
