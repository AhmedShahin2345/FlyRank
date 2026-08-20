# BE-03 · Stage 7 — AI vs me

## The prompt I wrote

I asked an AI assistant to build the same secured API, without copying from the
assignment sheet. This is the exact prompt I used:

---

> Build a secure FastAPI backend that uses Supabase Auth.
> - Create a `supabase` client using environment variables `SUPABASE_URL` and
>   `SUPABASE_KEY`.
> - Routes:
>   - `POST /auth/signup` — create a user with email + password (Supabase
>     `sign_up`), return 201.
>   - `POST /auth/login` — log in with email + password (Supabase
>     `sign_in_with_password`), return the access token and refresh token.
>   - `POST /auth/logout` — protected, calls Supabase `sign_out`, return 204.
>   - `GET /protected/profile` — protected, returns the logged-in user's info.
>   - `GET /protected/dashboard` — protected, returns a welcome message.
>   - `GET /public/info` — public, returns a static message.
> - Protect the /protected routes: check the `Authorization` header, call
>   `supabase.auth.get_user(token)` to verify, return 401 on failure.
> - Use `HTTPBearer` so Swagger shows an Authorize button.
> - Return 400 if email or password is missing on signup/login.

---

The AI's code is in [`ai-version/main.py`](ai-version/main.py), generated in
quarantine. My hand-built version (Stages 0–5) is untouched in the parent
folder.

## What I tested against it

- **Does it start?** Yes — it boots with a valid-format key.
- **Stage 3 checkpoint (tampered token):** sending a garbage token returns 401.
- **Stage 4 checkpoint (middleware reuse):** the AI version puts the token check
  inside the profile handler instead of a reusable dependency, so `/dashboard`
  is NOT actually protected.

## Diff vs my hand-built version

The concrete differences are analysed in the README's **"AI vs me"** section.

## Rematch

After the review I improved the prompt (added "extract the bearer token by
splitting on the space and taking the second part", "reject the request if the
header does not start with 'Bearer '", "put the verification in a reusable
dependency and apply it to every protected route", "never log the token"). The
regenerated version fixed the middleware reuse and added the prefix check, but
still returned FastAPI's default 422 for a missing body field unless I spelled
out the 400 validation step.