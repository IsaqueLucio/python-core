# Topic: Automated Testing with TestClient + pytest

Every endpoint so far has been tested MANUALLY, clicking around in
/docs. That doesn't scale: as your API grows, re-testing everything
by hand after every change becomes slow and unreliable. This topic
covers writing tests that run automatically and check your API's
behavior for you.

Coming from Spring Boot, think of it this way:
- pytest                        -> like JUnit
- TestClient                    -> like MockMvc / @SpringBootTest's
                                     TestRestTemplate -- simulates real
                                     HTTP requests against your app,
                                     without needing a running server
- app.dependency_overrides       -> like @MockBean in Spring -- swaps
                                     out a real dependency (a database
                                     session, an auth check) for a fake
                                     one, ONLY during tests
- pytest fixture                 -> like @BeforeEach / a JUnit
                                     extension providing shared setup

## Install the new dependency

    pip install pytest

(TestClient itself comes bundled with FastAPI/Starlette -- it uses
httpx internally, which you already installed in topic 10.)

## This folder's structure

    theory/11_testing/
    ├── database.py    # same generic setup from topic 8
    ├── models.py       # Item ORM model
    ├── schemas.py       # Pydantic schemas
    ├── main.py           # the actual API (nothing test-specific here)
    └── test_main.py       # the tests

## The core idea: TestClient

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}
```

`TestClient` lets you call your endpoints exactly like a real HTTP
client would (`.get()`, `.post()`, `.patch()`, `.delete()`...), but
without actually starting a server or making real network calls.
`assert` checks that something is true -- if it's false, pytest marks
that test as FAILED and shows you exactly what didn't match.

## The core idea: dependency_overrides

Your real `get_db` (topic 8) connects to `app.db`, the same file your
manual testing uses. If your automated tests wrote to THAT file, they
would pollute your real development data every time you ran them, and
worse, tests could interfere with each other depending on what data
already exists.

The fix: override `get_db` DURING TESTS ONLY, pointing it at a
completely separate, throwaway test database:

```python
app.dependency_overrides[get_db] = override_get_db
```

This is the same `Depends()` system from topic 6, just being told
"when someone asks for this dependency, use THIS other function
instead" -- purely for the test run. Your production code in main.py
never needs to know or care that this swap happened.

## How to run the tests

From INSIDE `theory/11_testing/`:

    pytest -v

`-v` (verbose) shows each individual test's name and PASSED/FAILED
status, instead of just a summary.

## Key takeaways

1. A test function must start with `test_` (that's how pytest finds
   them) -- `def test_something():`, not `def something_test():`.
2. `assert` is the core building block -- one test can have multiple
   assertions, each one checking a different part of the response.
3. `TestClient` doesn't require `uvicorn` to be running -- it talks
   directly to your FastAPI app in-process, which makes tests fast.
4. `dependency_overrides` is THE pattern for testing anything that
   depends on external resources (database, auth, third-party APIs)
   without touching the real thing.
5. Always clean up: `app.dependency_overrides.clear()` after tests
   (or use a fixture with teardown logic) so overrides from one test
   file don't leak into another.
