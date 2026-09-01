"""
Topic: Async / await

Every endpoint so far used `def`, not `async def`. Both work in
FastAPI, but they behave very differently under load. This topic
explains when each matters, and proves it with real timing, not just
theory.

Coming from Spring Boot / Java, think of it this way:
- A regular `def` endpoint  -> FastAPI runs it in a THREADPOOL
                                 (similar conceptually to a thread-per-
                                 request servlet model). It's safe for
                                 blocking code, but each request
                                 occupies a thread while it waits.
- An `async def` endpoint    -> runs directly on a SINGLE event loop
                                 (similar to Node.js's event loop, or
                                 Java's reactive/Netty-style non-
                                 blocking I/O). While it's `await`ing
                                 something (a network call, disk I/O),
                                 the event loop is FREE to handle other
                                 requests on that same thread.
- `await`                    -> "pause this function here, let other
                                 work run, resume me when this
                                 finishes" -- conceptually similar to
                                 a CompletableFuture callback, but
                                 written as if it were sequential code.

## The rule of thumb

- If your endpoint does I/O (calling another API, querying a database
  with an async driver, reading a file asynchronously) -> `async def`,
  and `await` every I/O call inside it.
- If your endpoint does CPU-bound work, or uses a library that doesn't
  support async (like the synchronous SQLAlchemy session from topic 8)
  -> keep it as plain `def`. FastAPI's threadpool handles it safely.
- The ONE thing to NEVER do: write `async def` and then call a
  BLOCKING function inside it without awaiting anything async. That
  freezes the entire event loop -- every other request, from every
  other user, waits until that one blocking call finishes. This is
  the single most common async mistake in FastAPI.

## Install the new dependency

    pip install httpx

httpx is like `requests`, but with async support -- used any time your
API needs to CALL another API (a common need in real backends: calling
a payment provider, a third-party service, another microservice...).

## How to run this file

    uvicorn 10_async.10_async_theory:app --reload

(single-file topic again, like topics 1-6 -- this concept is about
understanding a mechanism, not building a layered project)
"""

import asyncio
import time

import httpx
from fastapi import FastAPI

app = FastAPI(
    title="Learning FastAPI",
    description="Async / await example",
    version="0.1.0",
)


# --- The wrong way: blocking inside async def ---
@app.get("/bad-async")
async def bad_async_example():
    """
    THIS IS THE MISTAKE TO AVOID. time.sleep() is a BLOCKING call --
    it doesn't yield control back to the event loop. Even though this
    function is `async def`, this specific line freezes EVERYTHING:
    no other request (from any user) can be processed while this
    line runs. Never do this in a real project.
    """
    time.sleep(2)  # BLOCKING -- freezes the whole server for 2 seconds
    return {"message": "This blocked everyone else for 2 seconds"}


# --- The correct way: a truly async, non-blocking endpoint ---
@app.get("/good-async")
async def good_async_example():
    """
    asyncio.sleep() is the ASYNC equivalent of time.sleep(): it pauses
    THIS request for 2 seconds, but hands control back to the event
    loop during that time, so other requests keep being processed.
    """
    await asyncio.sleep(2)  # NON-blocking -- event loop stays free
    return {"message": "This did NOT block anyone else"}


# --- A regular sync endpoint (still perfectly fine!) ---
@app.get("/sync")
def sync_example():
    """
    This uses plain `def`. FastAPI automatically runs this in a
    threadpool, so time.sleep() here does NOT freeze the whole
    server -- it only occupies one thread from the pool. For
    endpoints using the synchronous SQLAlchemy session from topic 8,
    THIS is the correct choice -- don't force `async def` onto
    blocking database code.
    """
    time.sleep(2)
    return {"message": "Blocked only one thread, not the whole server"}


# --- Real-world async: calling an external API ---
@app.get("/external-call")
async def call_external_api():
    """
    This is the actual common use case for async in a real backend:
    your API calling ANOTHER API (a payment gateway, a weather
    service, a third-party integration...). httpx.AsyncClient lets
    you `await` that network call instead of blocking on it.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.github.com")
    return {"status_code": response.status_code}


# --- Running multiple async calls CONCURRENTLY ---
@app.get("/external-calls-parallel")
async def call_multiple_apis_in_parallel():
    """
    asyncio.gather() runs multiple awaitables AT THE SAME TIME,
    instead of one after another. If each call takes ~1 second, THREE
    sequential calls would take ~3 seconds total -- but gathered
    together, they all finish in ~1 second, since they're all
    "in flight" simultaneously.
    """
    async with httpx.AsyncClient() as client:
        responses = await asyncio.gather(
            client.get("https://api.github.com"),
            client.get("https://api.github.com/zen"),
            client.get("https://api.github.com/octocat"),
        )
    return {"statuses": [r.status_code for r in responses]}


# Key takeaways:
# 1. `async def` + `await` = non-blocking, good for I/O (network, disk).
# 2. Plain `def` = FastAPI's threadpool handles it, good for blocking/
#    CPU-bound code, or libraries without async support.
# 3. NEVER call a blocking function (time.sleep, a sync DB call,
#    a sync requests.get) inside `async def` without awaiting it --
#    that freezes the entire server for every user.
# 4. `httpx.AsyncClient` is the standard tool for making async HTTP
#    calls to other APIs from inside a FastAPI endpoint.
# 5. `asyncio.gather(...)` runs multiple async operations concurrently,
#    turning what would be sequential wait time into parallel wait time.