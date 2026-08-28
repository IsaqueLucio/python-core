# Topic: Authentication with JWT / OAuth2

Every endpoint so far has been open to anyone. Real APIs need to know
WHO is calling, and whether they're allowed to. This topic covers the
standard FastAPI pattern: register a user with a hashed password, log
in to receive a JWT (JSON Web Token), and protect endpoints so they
only work with a valid token.

Coming from Spring Boot, think of it this way:
- passlib (password hashing)  -> like BCryptPasswordEncoder
- JWT access token             -> same concept as Spring Security's
                                   JWT filter chain, just issued and
                                   verified manually here instead of
                                   through a security config class
- OAuth2PasswordBearer         -> tells FastAPI's /docs how to send
                                   the token (Authorization: Bearer ...),
                                   similar to declaring a security
                                   scheme in Spring/OpenAPI config
- Depends(get_current_user)    -> the FastAPI equivalent of a
                                   @PreAuthorize / SecurityContext
                                   check, built directly on Depends()
                                   from topic 6

## Install the new dependencies

    pip install "passlib[bcrypt]" "python-jose[cryptography]"

- `passlib` -> hashes and verifies passwords (NEVER store plain text
  passwords in a database, ever).
- `python-jose` -> creates and decodes JWT tokens.

## This folder's structure

    theory/09_auth/
    ├── database.py   # same generic setup from topic 8
    ├── models.py     # User ORM model
    ├── schemas.py    # UserCreate, UserOut, Token
    ├── auth.py       # password hashing + JWT creation/verification
    └── main.py       # register, login, and a protected endpoint

## How the flow works, end to end

1. `POST /register` -- client sends username + plain password. The
   server HASHES the password (never stores it as-is) and saves the
   user in the database.
2. `POST /login` -- client sends username + password again. The
   server looks up the user, verifies the password against the
   stored hash, and if it matches, generates a JWT access token
   containing the username and an expiration time.
3. The client stores that token and sends it on every future request,
   in a header: `Authorization: Bearer <token>`.
4. Protected endpoints use `Depends(get_current_user)`, which:
   - reads the token from the Authorization header (automatically,
     via OAuth2PasswordBearer)
   - decodes and verifies it (checks the signature and expiration)
   - looks up the corresponding user
   - raises HTTPException(401) if anything is invalid/expired
   - otherwise, injects the user into the endpoint

## How to run this example

From INSIDE `theory/09_auth/`:

    uvicorn main:app --reload

## Key takeaways

1. NEVER store plain-text passwords. `passlib` handles hashing with
   bcrypt, a slow-by-design algorithm that resists brute-force attacks.
2. A JWT is not encrypted, just signed -- anyone can decode and READ
   its contents, but they can't FORGE a valid one without your secret
   key. Never put sensitive data (like a password) inside a token.
3. `OAuth2PasswordBearer(tokenUrl="login")` doesn't do authentication
   itself -- it just tells FastAPI (and the /docs UI) where to send
   the username/password to get a token, and how to read tokens from
   future requests.
4. `Depends(get_current_user)` is just another dependency, exactly
   like topic 6 -- the only difference is WHAT it checks (a valid
   token instead of a header value).
5. This is a simplified, educational implementation. Production
   systems add refresh tokens, token revocation/blacklisting, rate
   limiting on login attempts, and stronger secret management
   (environment variables, secret managers) -- some of this is
   covered in topic 12.
