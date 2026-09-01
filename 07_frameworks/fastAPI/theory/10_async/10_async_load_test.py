"""
This script PROVES the difference between /bad-async, /good-async and
/sync from theory/10_async.py, by firing several requests at each
endpoint AT THE SAME TIME and measuring the total time.

How to use:
    1. In one terminal, run the app:
         uvicorn theory.10_async:app --reload
    2. In ANOTHER terminal (same venv), run this script:
         python theory/10_async_load_test.py

What you should observe (each endpoint sleeps for 2 seconds):
    /bad-async   with 5 concurrent requests -> ~10 seconds total
                 (2s x 5, because it blocks the whole server --
                 requests get processed one at a time despite being
                 "concurrent" from the client's side)
    /good-async  with 5 concurrent requests -> ~2 seconds total
                 (all 5 requests are handled at once, non-blocking)
    /sync        with 5 concurrent requests -> ~2 seconds total
                 (FastAPI's threadpool handles multiple sync requests
                 concurrently too, up to its thread pool size -- this
                 is why plain `def` is still fine for many cases)

This is the actual, measurable proof of the "never block inside
async def" warning from the theory file -- it's not just a rule to
memorize, you can literally watch it happen.
"""

import asyncio
import time

import httpx

BASE_URL = "http://127.0.0.1:8000"
CONCURRENT_REQUESTS = 5


async def hit_endpoint(client: httpx.AsyncClient, path: str) -> None:
    await client.get(f"{BASE_URL}{path}")


async def measure(path: str) -> None:
    async with httpx.AsyncClient(timeout=30.0) as client:
        start = time.perf_counter()
        await asyncio.gather(*[hit_endpoint(client, path) for _ in range(CONCURRENT_REQUESTS)])
        elapsed = time.perf_counter() - start
    print(f"{path:<25} -> {CONCURRENT_REQUESTS} concurrent requests took {elapsed:.2f}s")


async def main():
    print(f"Firing {CONCURRENT_REQUESTS} concurrent requests at each endpoint...\n")
    await measure("/bad-async")
    await measure("/good-async")
    await measure("/sync")


if __name__ == "__main__":
    asyncio.run(main())