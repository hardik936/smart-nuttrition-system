# Deploying Smart Nutrition System on Railway (Free-Friendly Setup)

This guide deploys the project as **three Railway services**:
1. Backend API (FastAPI)
2. Frontend (React + Nginx)
3. PostgreSQL database

> Railway free availability can change over time (trial credits / hobby limits), but this is currently one of the easiest alternatives to Render for this repo.


## Quick start (exactly what to do now)

1. Push this repository to GitHub.
2. In Railway, create a project and add:
   - PostgreSQL service
   - Backend service (from this repo root `Dockerfile`)
   - Frontend service (from `frontend/Dockerfile`)
3. In backend service variables, set:
   - `DATABASE_URL` (from Railway PostgreSQL)
   - `SECRET_KEY` (use a long random value)
4. Deploy backend and copy its public URL.
5. In frontend service variables, set:
   - `VITE_API_URL` = backend public URL
6. Redeploy frontend (important; Vite env vars are baked at build time).
7. Open frontend URL -> register user -> login.

If you want, I can also prepare deployment for Fly.io as a backup.

## 1) Create a Railway project

- Sign in to Railway and create a new project.
- Connect this GitHub repository.

## 2) Provision PostgreSQL

- Add a **PostgreSQL** service in the same Railway project.
- Railway will provide a connection string (usually as `DATABASE_URL`).

## 3) Deploy backend service

Create a new service from this repo and set:

- **Root Directory:** `/` (repo root)
- **Dockerfile Path:** `Dockerfile`
- **Port:** `8000`
- **Start Command:** (from Dockerfile) `uvicorn main:app --host 0.0.0.0 --port 8000`

Backend environment variables:

- `DATABASE_URL` = value from Railway Postgres
- `SECRET_KEY` = strong random string (required for stable JWT behavior)
- `PORT` = `8000` (optional in Railway, but safe)

Health check path:

- `/`

Expected healthy response:

```json
{"message":"NutriTrack API is running"}
```

## 4) Deploy frontend service

Create another service from this repo and set:

- **Root Directory:** `frontend`
- **Dockerfile Path:** `frontend/Dockerfile`
- **Port:** `80`

Frontend environment variable:

- `VITE_API_URL` = your backend public URL (example: `https://smart-nutrition-backend.up.railway.app`)

Important: since Vite injects env vars at build time, redeploy frontend after changing `VITE_API_URL`.

## 5) Verify login/register flow

From the deployed frontend:

- Register a new user
- Login with that user
- Confirm authenticated pages load

If login/register fails:

- Check frontend `VITE_API_URL`
- Check backend logs for `/auth/register` and `/auth/token`
- Confirm backend `DATABASE_URL` is set and database is reachable
- Confirm `SECRET_KEY` is set (not empty)

## 6) Optional hardening

- Restrict CORS origins in `backend/main.py` to your frontend domain.
- Rotate `SECRET_KEY` and keep it in Railway environment secrets.
- Add persistent volume only if you keep SQLite (Postgres recommended in production).

## Quick deployment checklist

- [ ] Railway Postgres created
- [ ] Backend deployed from root `Dockerfile`
- [ ] Backend `DATABASE_URL` + `SECRET_KEY` set
- [ ] Frontend deployed from `frontend/Dockerfile`
- [ ] Frontend `VITE_API_URL` points to backend URL
- [ ] Login and registration verified in browser

## Common login/register issues after deploy

1. **Frontend still points to wrong API URL**
   - Symptom: Register/login fails from UI but backend works directly.
   - Fix: Ensure frontend `VITE_API_URL` matches backend public URL and redeploy frontend.

2. **Backend cannot reach database**
   - Symptom: `/auth/register` returns 500 in backend logs.
   - Fix: Confirm backend `DATABASE_URL` is set from the Railway PostgreSQL service.

3. **Missing/weak JWT secret**
   - Symptom: Token/auth inconsistencies after restart.
   - Fix: Set a stable backend `SECRET_KEY` and redeploy backend.

4. **Backend health check fails**
   - Symptom: Service restarts continuously.
   - Fix: Health check path should be `/` and backend should return `{"message":"NutriTrack API is running"}`.

