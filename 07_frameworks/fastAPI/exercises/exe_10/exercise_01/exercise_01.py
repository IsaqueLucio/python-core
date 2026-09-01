"""
Exercise 1: Find and fix the blocking mistake

Goal:
    Practice recognizing the most common async mistake in FastAPI --
    blocking code inside `async def` -- and fixing it.

Instructions:
    1. Create the FastAPI app instance.
    2. Below is a BROKEN endpoint, already written for you (don't
       change its name or path). It's meant to simulate a slow
       "report generation" process, but it has the classic mistake:

       @app.get("/reports/slow")
       async def generate_report_broken():
           time.sleep(3)  # <- THIS is the bug
           return {"report": "done"}

       Copy it in as-is first, and confirm you understand WHY it's
       broken (re-read the "wrong way" example in theory/10_async.py
       if needed).

    3. Now write a SECOND endpoint, `/reports/fast`, that does the
       SAME thing (simulates a 3-second report generation) but the
       CORRECT way -- non-blocking.

    4. Write a THIRD endpoint, `/reports/fast-sync`, that also
       simulates the same 3-second delay, but using plain `def`
       instead of `async def` (still using time.sleep -- this is
       fine here, since FastAPI's threadpool handles it).

Run it with:
    uvicorn exercise_01:app --reload

Test it:
    Use the load test pattern from theory/10_async_load_test.py --
    adapt it (or write your own small script) to fire 3 concurrent
    requests at /reports/slow, then at /reports/fast, then at
    /reports/fast-sync, and compare the total time for each.
    You should see /reports/slow take ~9 seconds (3s x 3, blocking),
    while the other two take ~3 seconds each.
"""

import asyncio
import time

from fastapi import FastAPI

app = FastAPI(
    title="Learning FastAPI: Exercise 1",
    description="Find and fix the blocking mistake",
    version="0.1.0",
)


@app.get("/reports/slow")
async def generate_report_broken():
    time.sleep(3)  # BUG: blocking call inside async def
    return {"report": "done (but blocked everyone else)"}


# TODO: define GET "/reports/fast" (async def, using asyncio.sleep(3))
@app.get("/reports/fast")
async def get_resports_async():
    await asyncio.sleep(3)
    return {"report": "done (usimg asyncio.sleep(3))"}

# TODO: define GET "/reports/fast-sync" (plain def, using time.sleep(3))
@app.get("/reports/fast-sync")
def get_reports_fast_sync():
    time.sleep(3)
    return {"report": "done (plain def, using time.sleep(3)"}
