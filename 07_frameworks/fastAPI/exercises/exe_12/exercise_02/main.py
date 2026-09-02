"""
See INSTRUCTIONS.md for the full task description.
"""

import asyncio
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# TODO: create the FastAPI app instance
app = FastAPI()

# TODO: add CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["*"], 
    allow_headers=["*"]
)

# TODO: define the add_process_time_header middleware
# @app.middleware("http")
# async def add_process_time_header(request, call_next):
#     measure elapsed time around call_next, add it as
#     response.headers["X-Process-Time"], return the response
@app.middleware("http")
async def add_process_time_header(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start
    response.headers["X-Process-Time"] = str(elapsed)
    return response

# TODO: GET "/fast" endpoint returning {"message": "quick"} immediately
@app.get("/fast")
def get_fast():
    return {"message": "quick"}

# TODO: GET "/slow" endpoint that awaits asyncio.sleep(1) before
# returning {"message": "slow"}
@app.get("/slow")
async def get_slow():
    await asyncio.sleep(3)
    return {"message": "slow"}
