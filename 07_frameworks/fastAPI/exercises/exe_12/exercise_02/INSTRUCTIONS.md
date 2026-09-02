# Exercise 2: CORS + a custom logging middleware

## Goal
Practice configuring CORS for a specific frontend origin, and writing
your own middleware that adds a custom response header AND logs
timing -- combining both middleware patterns from the theory file.

## Structure to build

    exercise_02/
    └── main.py

## Instructions

1. Create the FastAPI app instance.

2. Add CORSMiddleware, but this time allow TWO origins (simulating a
   project with both a local dev frontend and a staging frontend):
   `allow_origins=["http://localhost:3000", "http://localhost:5173"]`
   (5173 is Vite's default dev port, a common React/Vue setup)
   allow_methods=["*"], allow_headers=["*"]

3. Write a custom middleware `add_process_time_header` that:
   - records the start time (time.perf_counter())
   - calls `response = await call_next(request)`
   - calculates elapsed time
   - adds a CUSTOM HEADER to the response before returning it:
     `response.headers["X-Process-Time"] = str(elapsed)`
     (this is a genuinely common real-world pattern: exposing timing
     information via a response header, which browser dev tools and
     API clients can inspect directly, instead of only being visible
     in your server's own logs)
   - returns the response

4. Add two simple endpoints to test with:
   - `GET "/fast"` returning `{"message": "quick"}` immediately
   - `GET "/slow"` that does `await asyncio.sleep(1)` (topic 10!)
     before returning `{"message": "slow"}`

## Run it

    uvicorn main:app --reload

## Test it

In http://127.0.0.1:8000/docs, call GET /fast and GET /slow. The
Swagger UI doesn't show response headers by default in every version,
so also try this from a terminal, which shows headers clearly:

    curl -i http://127.0.0.1:8000/fast
    curl -i http://127.0.0.1:8000/slow

Look for a line like `x-process-time: 0.00123` in the curl output for
/fast, and something close to `1.00...` for /slow -- confirming your
middleware is measuring and exposing real timing per request.
