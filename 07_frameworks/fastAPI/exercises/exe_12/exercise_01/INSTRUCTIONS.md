# Exercise 1: Move secrets out of the code

## Goal
Take the hardcoded SECRET_KEY pattern from topic 9 and fix it for
real, using pydantic-settings -- this is the exercise that finally
pays off that "never hardcode this in a real project" warning.

## Structure to build

    exercise_01/
    ├── .env.example
    ├── .env             (you create this locally, NOT provided --
    │                      it should never be shared/committed)
    ├── config.py
    └── auth.py

## Instructions

1. In `.env.example`, list (WITHOUT real values, just placeholders):
   ```
   SECRET_KEY=change-this-to-a-long-random-string
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

2. Create your own `.env` (copy .env.example, then edit it) with:
   - a real random secret_key of your choosing (any long random
     string is fine for practice -- in a real project you'd generate
     one with, e.g., `openssl rand -hex 32`)
   - the same ALGORITHM and ACCESS_TOKEN_EXPIRE_MINUTES as the example

3. In `config.py`:
   - Define `class Settings(BaseSettings):` with fields secret_key
     (str, required), algorithm (str, default "HS256"),
     access_token_expire_minutes (int, default 30)
   - Add `class Config: env_file = ".env"` inside it
   - Create `settings = Settings()` at module level

4. In `auth.py` (rewrite the topic 9 version to use Settings instead
   of hardcoded constants):
   - `from config import settings`
   - Remove the hardcoded `SECRET_KEY`, `ALGORITHM`,
     `ACCESS_TOKEN_EXPIRE_MINUTES` constants entirely
   - Everywhere those were used (in create_access_token and
     decode_access_token), use `settings.secret_key`,
     `settings.algorithm`, `settings.access_token_expire_minutes`
     instead
   - Copy the rest of the JWT logic (create_access_token,
     decode_access_token) unchanged from topic 9

## Verify it works

    python -c "from config import settings; print(settings.secret_key)"

Should print YOUR real secret key from `.env` -- proving the settings
are actually being read from the file, not hardcoded anywhere.

Then try temporarily renaming `.env` to something else and running
the same command again -- it should now raise a validation error
(secret_key is required and has no default), proving Settings truly
depends on that file being present, not silently falling back to
something hardcoded.
