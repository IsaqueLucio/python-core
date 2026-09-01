"""
Exercise 3: Parallel calls with asyncio.gather

Goal:
    Practice fetching data from MULTIPLE external sources at once,
    instead of one after another -- the biggest real-world performance
    win async gives you.

Instructions:
    1. Create the FastAPI app instance.
    2. Create a GET "/weather-sequential" endpoint (async def) that
       calls the wttr.in API (same pattern as exercise 2) for THREE
       hardcoded cities: "London", "Tokyo", "Franca" -- one AFTER the
       other (three separate `await client.get(...)` calls, in
       sequence, NOT using gather). Return a list of
       {"city": ..., "temperature_c": ...} for all three.

    3. Create a GET "/weather-parallel" endpoint (async def) that
       does the EXACT SAME THING, but using asyncio.gather() to fire
       all three requests at once (same pattern as the theory file's
       /external-calls-parallel). Return the same shape of data.

    4. Add a `time.perf_counter()` measurement inside BOTH endpoints:
       record the time before the calls, record it again after, and
       include an extra field in the response:
       {"elapsed_seconds": round(elapsed, 2), "results": [...]}

Run it with:
    uvicorn exercise_03:app --reload

Test in http://127.0.0.1:8000/docs:
    GET /weather-sequential -> note the elapsed_seconds
    GET /weather-parallel    -> note the elapsed_seconds

    /weather-parallel should be noticeably faster than
    /weather-sequential (roughly: sequential takes about 3x as long
    as a single call, parallel takes about the same as a single call,
    since all three run at once).

    Note: wttr.in's response time varies depending on their server
    load, so times won't be perfectly consistent between runs -- focus
    on the RELATIVE difference between the two endpoints, not exact
    numbers.
"""

import asyncio
import time

import httpx
from fastapi import FastAPI, HTTPException

CITIES = ["London", "Tokyo", "Franca"]

# TODO: create the FastAPI app instance
app = FastAPI()

# TODO: GET "/weather-sequential" endpoint (async def)
# loop over CITIES, awaiting one httpx call at a time (no gather)
# measure elapsed time, return {"elapsed_seconds": ..., "results": [...]}
@app.get("/weather-sequential")
async def get_weather_sequential():
    results = []
    start = time.perf_counter()
    for city in CITIES:
        async with httpx.AsyncClient() as client:
            try:
                url = f"https://wttr.in/{city}?format=j1"
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                result = {
                    "city": city,
                    "temperature_c": data["current_condition"][0]["temp_C"]
                }
                results.append(result)
            except HTTPException as e:
                return f"[ERROR] {e}."
    elapsed = time.perf_counter() - start

    return {"elapsed_seconds": elapsed, "results": results}

# TODO: GET "/weather-parallel" endpoint (async def)
# use asyncio.gather() to fire all requests to CITIES at once
# measure elapsed time, return {"elapsed_seconds": ..., "results": [...]}
@app.get("/weather-parallel")
async def get_weather_parallel():

    start = time.perf_counter()
    async def support_function(city: str):
        url = f"https://wttr.in/{city}?format=j1"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                return {
                    "city": city,
                    "temperature_c": data["current_condition"][0]["temp_C"] 
                }
            except (httpx.RequestError, KeyError, IndexError) as e:
                return f"[ERROR] {e}."
    tasks = [support_function(city) for city in CITIES]
    results = await asyncio.gather(*tasks)
    elapsed_time = time.perf_counter() - start
    return {
        "elapsed_seconds": round(elapsed_time, 2),
        "results": results
    }