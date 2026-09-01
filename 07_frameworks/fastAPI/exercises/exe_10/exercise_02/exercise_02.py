"""
Exercise 2: Calling an external API asynchronously

Goal:
    Practice the actual real-world use case for async in a backend:
    YOUR api calling ANOTHER api, without blocking while it waits.

Instructions:
    1. Create the FastAPI app instance.
    2. Create a GET "/weather/{city}" endpoint (async def) that:
       - uses httpx.AsyncClient() (as an async context manager, like
         the theory example) to call this free, no-auth-required API:
         f"https://wttr.in/{city}?format=j1"
       - awaits the response
       - if response.status_code != 200, raise
         HTTPException(502, "Weather service unavailable")
       - otherwise, parse response.json() and return just:
         {"city": city, "temperature_c": <value>}

         Hint: wttr.in's JSON response has the current temperature at
         data["current_condition"][0]["temp_C"] -- explore the raw
         JSON response first (e.g. print it, or check it in the
         browser at https://wttr.in/London?format=j1) to see the full
         structure before writing the parsing code.

    3. Create a SECOND endpoint, GET "/weather-broken/{city}", that
       does the SAME thing but WRONG on purpose: use the plain
       (synchronous) `requests` library instead of httpx, INSIDE an
       `async def` function, without any await. (You'll need
       `pip install requests` if you don't have it.) This lets you
       feel the difference: it will still "work" for a single
       request, but now you understand WHY it's still a mistake, even
       though nothing crashes -- explain in a code comment why this
       second endpoint has the same problem as /bad-async from the
       theory file.

Run it with:
    uvicorn exercise_02:app --reload

Test in http://127.0.0.1:8000/docs:
    GET /weather/London      -> should return a temperature
    GET /weather/Franca       -> try your own city!
    GET /weather-broken/London -> also "works", but re-read your own
    comment before moving on -- make sure you can explain why it's
    still wrong practice.
"""

from fastapi import FastAPI, HTTPException
import httpx, requests

# TODO: create the FastAPI app instance
app = FastAPI()

# TODO: GET "/weather/{city}" endpoint (async def)
# use httpx.AsyncClient(), await the call to
# f"https://wttr.in/{city}?format=j1"
# raise HTTPException(502, "Weather service unavailable") on failure
# return {"city": city, "temperature_c": <value from the JSON>}
@app.get("/weather/{city}")
async def get_weather_city(city: str):
    url = f"https://wttr.in/{city}?format=j1"
    try:
      async with httpx.AsyncClient() as client:
          response = await client.get(url)
      if response.status_code == 502:
           raise HTTPException(status_code=502, detail="Weather service unavailable")
      response.raise_for_status()
      data = response.json()
      temp = data["current_condition"][0]["temp_C"]
      return {
           "city": city, 
           "temperature_c": temp
           }
    except HTTPException as e:
        raise

# TODO: GET "/weather-broken/{city}" endpoint (async def, but WRONG)
# use the synchronous `requests` library (pip install requests)
# without awaiting anything -- add a comment explaining why this is
# still a mistake, even though the endpoint "works"
@app.get("/weather-broken/{city}")
async def get_broken_Weather(city: str):
    """
    WRONG implementation: Uses synchronous 'requests' inside an async function.
    
    PROBLEM EXPLANATION:
    This endpoint uses the synchronous `requests` library inside an `async def`
    function. The `requests.get()` call is BLOCKING - it will freeze the entire
    event loop while waiting for the external API response. During this time,
    the server cannot handle ANY other requests, even though the function is
    defined with `async def`. This defeats the entire purpose of using async.
    
    For a single request, it works fine and you won't notice the problem.
    But with many concurrent users, this endpoint will cause:
    - Increased response times
    - Event loop starvation
    - Poor scalability
    - Could even cause timeout errors under high load
    
    The correct approach is the /weather endpoint using httpx.AsyncClient()
    with await, which properly yields control back to the event loop while
    waiting for the external API response.
    """
    url = f"https://wttr.in/{city}?format=j1"
    try:
        response = requests.get(url)
        if response.status_code == 502:
            raise HTTPException(status_code=502, detail="Weather service unavailable")
        response.raise_for_status()
        data = response.json()
        temp = data["current_condition"][0]["temp_C"]
        return {
           "city": city, 
           "temperature_c": temp
           }
    except HTTPException as e:
         raise