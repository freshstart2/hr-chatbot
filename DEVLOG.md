<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Generate Day 3 markdown with complete context for a new session to pick up from this point without any loss of information. Also, publish the code so far in the git repo to access it via a new session to refresh your context for any abrupt disruption.

Here is the complete Day 3 handoff document. Save this as `DEVLOG.md` in the root of your project.

***

```markdown
# HR Analytics Chatbot — Development Log

## Project Overview

An HR Analytics chatbot that allows HR analysts, managers, and admins to query
employee data using natural language. Built on a local LLM (Ollama) with a
FastAPI backend, React frontend, Cube.js for metrics, and PostgreSQL as the
database.

---

## Tech Stack

| Layer       | Technology                        |
|-------------|-----------------------------------|
| Frontend    | React + Vite + TypeScript         |
| Backend     | FastAPI (Python 3.11)             |
| LLM         | Ollama (local) — model TBD        |
| Metrics     | Cube.js                           |
| Database    | PostgreSQL 15 (Alpine)            |
| Auth        | JWT (HS256)                       |
| Deployment  | Docker Compose (Windows host)     |

---

## Project Structure

```

C:\AIAgent\hr-chatbot\
├── docker-compose.yml
├── .env
├── infrastructure/
│   └── db/
│       ├── schema.sql          ← 01_schema
│       ├── rls_policies.sql    ← 02_rls
│       ├── seed_data.sql       ← 03_seed (generated, do not edit manually)
│       └── generate_seed.py   ← run on Windows host to regenerate seed
├── backend/
│   ├── Dockerfile
│   ├── main.py                 ← Day 3 target
│   ├── db/
│   │   ├── session.py          ← Day 3 target
│   │   └── models.py           ← Day 3 target
│   ├── auth/
│   │   ├── jwt_handler.py      ← Day 3 target
│   │   └── dependencies.py     ← Day 3 target
│   ├── routers/
│   │   └── auth.py             ← Day 3 target
│   └── llm/
│       └── client.py           ← Day 3 target
├── frontend/
│   ├── Dockerfile
│   ├── src/
│   ├── public/
│   ├── index.html
│   └── vite.config.ts
└── cube/
└── schema/                 ← Day 4 target (Cube.js data models)

```

---

## Database Schema — All 7 Tables (hr schema)

### hr.employees (core — 32 columns)
Aligned with Demographics-1.csv (30 original columns) + salary + created_at

```

id, first_name, last_name, email,
gender, date_of_birth,
business_title, level,
primary_skill, secondary_skill,
employment_category, employment_type, employment_status,
work_mode, work_city, work_country, work_state,
start_date, termination_date, last_promotion_date, last_job_change_date,
supervisor_first_name, supervisor_last_name, supervisor_id (FK → employees.id),
department_l1, department_l2, department_l3,
hr_bp_name, job_project, job_client,
termination_reason, salary, created_at

```

### hr.employee_exits
```

id, employee_id (FK → employees.id), exit_date, exit_type, reason, created_at

```

### hr.performance_reviews
```

id, employee_id (FK → employees.id), review_date, rating (1.0–5.0),
reviewer_id (FK → employees.id), created_at

```

### hr.hiring_requisitions
```

id, department, open_date, close_date, status (open|filled|cancelled), created_at
NOTE: days_open is NOT a column — compute as:
COALESCE(close_date, CURRENT_DATE) - open_date in queries

```

### hr.users (app auth)
```

user_id, name, email, hashed_password, role (analyst|manager|hr_admin),
employee_id (FK → employees.id, nullable), created_at

```

### hr.query_audit_log
```

id, user_id (FK → users.user_id), role, query_text, resolved_query,
metric_id, execution_type (metric_route|llm_generated), execution_ms,
cache_hit, session_id, turn_number, created_at

```

### hr.conversation_sessions
```

session_id (PK, VARCHAR), user_id (FK → users.user_id),
turns (JSONB default '[]'), created_at, updated_at

```

---

## Seed Data — Verified State

```

Total employees:     500
Active:              310
Inactive:            190
employee_exits:      190  (matches Inactive exactly)
Departments:         Engineering(114), Product Development(90),
Analytics(77), Sales(77), Marketing(47),
Finance(35), Human Resource(31), Business analyst(29)
App users (hr.users):
analyst@hr.com    / password: analyst123   / role: analyst
manager@hr.com    / password: manager123   / role: manager
hr_admin@hr.com   / password: admin123     / role: hr_admin

```

---

## RLS Policies — Active on 2 Tables

### hr.employees
- `hr_admin` role → sees ALL rows
- `manager` role → sees only rows where supervisor_id = app.user_id
- `analyst` role → sees only Active employees

### hr.performance_reviews
- `hr_admin` role → sees ALL reviews
- `manager` role → sees reviews for their direct reports only
- `analyst` role → sees ALL reviews

RLS is enforced via PostgreSQL session variables:
```sql
SET app.user_role = 'manager';
SET app.user_id   = '3';
```

These must be set at the start of every database session in the backend.

---

## Docker Compose Services

| Container | Image | Port | Status |
| :-- | :-- | :-- | :-- |
| hr_postgres | postgres:15-alpine | 5432 | ✅ Healthy |
| hr_ollama | ollama/ollama:latest | 11434 | ✅ Running |
| hr_cubejs | cubejs/cube:latest | 4000 | ⏳ Pending |
| hr_backend | hr-chatbot-backend | 8000 | ⏳ Pending |
| hr_frontend | hr-chatbot-frontend | 3000 | ⏳ Pending |


---

## .env Variables (structure — not values)

```
POSTGRES_DB=hr_analytics
POSTGRES_USER=hr_admin
POSTGRES_PASSWORD=<secret>
CUBEJS_DB_TYPE=postgres
CUBEJS_DB_HOST=postgres
CUBEJS_DB_NAME=hr_analytics
CUBEJS_DB_USER=hr_admin
CUBEJS_DB_PASS=<secret>
CUBEJS_API_SECRET=<secret>
OLLAMA_BASE_URL=http://hr_ollama:11434
JWT_SECRET=<secret>
JWT_ALGORITHM=HS256
ENVIRONMENT=development
```


---

## Day 3 — What Needs to Be Built

Before starting Day 3, provide:

1. Contents of `backend/Dockerfile`
2. Output of: `docker exec -it hr_ollama ollama list`

### Day 3 File Build Order

#### Step 1 — `backend/main.py`

- FastAPI app instantiation
- CORS middleware (allow localhost:3000)
- Register routers: `/api/auth`, `/api/chat`, `/api/metrics`
- Health check: `GET /health`
- RLS session variable injection middleware


#### Step 2 — `backend/db/session.py`

- Async SQLAlchemy engine using `DATABASE_URL` from env
- `AsyncSession` factory
- `get_db` dependency for FastAPI
- Set `app.user_role` and `app.user_id` on every new connection


#### Step 3 — `backend/db/models.py`

- SQLAlchemy ORM models for all 7 tables
- All column types must match schema.sql exactly
- `supervisor_id` self-referential FK on Employee model


#### Step 4 — `backend/auth/jwt_handler.py`

- `create_access_token(data: dict) → str`
- `verify_token(token: str) → dict`
- Uses `JWT_SECRET` and `JWT_ALGORITHM` from env
- Token expiry: 8 hours


#### Step 5 — `backend/auth/dependencies.py`

- `get_current_user` FastAPI dependency
- Reads Bearer token from Authorization header
- Returns user dict with `user_id`, `role`, `email`


#### Step 6 — `backend/routers/auth.py`

- `POST /api/auth/login`
    - Body: `{ email, password }`
    - Verifies bcrypt hash against `hr.users`
    - Returns: `{ access_token, token_type, role, name }`


#### Step 7 — `backend/llm/client.py`

- Async HTTP client wrapping Ollama REST API
- `generate(prompt: str, model: str) → str`
- `chat(messages: list, model: str) → str`
- Retry logic: 3 attempts with 2s backoff
- Base URL from `OLLAMA_BASE_URL` env var

---

## Day 4 Preview — Cube.js Schema

After Day 3 backend is verified:

- `cube/schema/Employees.js`
- `cube/schema/Attrition.js`
- `cube/schema/Headcount.js`
- `cube/schema/Performance.js`

---

## Day 5 Preview — Chat Endpoint

- `POST /api/chat`
- Intent classifier → metric_route OR llm_generated
- Metric router maps intent → Cube.js query
- LLM fallback for open-ended questions
- Conversation memory (session-based)
- Audit logging to `hr.query_audit_log`

---

## Key Decisions Made

| Decision | Reason |
| :-- | :-- |
| `supervisor_id` not `manager_id` | Matched CSV column naming convention |
| `days_open` removed from hiring_requisitions | `CURRENT_DATE` is not immutable — cannot use in GENERATED ALWAYS AS |
| Seed runs on Windows host (not container) | Faker + bcrypt installed locally via pip |
| `DO $ IF NOT EXISTS $` for CREATE ROLE | `hr_admin` is a built-in PostgreSQL 15 role |
| `frontend` volumes mount only src/public/index/vite | Prevents Windows node_modules from overwriting container node_modules |
| RLS via `current_setting('app.user_role')` | Stateless per-request enforcement without separate DB users |


---

## Session Rules (apply to ALL sessions on this project)

- Complete file code only — no snippets, no partial blocks
- Never assume things not in context — ask first
- Audit before generating — cross-check all column/table/role names
- One file at a time — wait for confirmation before next file

```

***

## Git Push Commands

Run these now to push everything to GitHub so any new session can pull full context:

```cmd
cd C:\AIAgent\hr-chatbot
git add .
git commit -m "feat: Day 2 complete — schema, RLS, seed, DEVLOG added"
git push origin main
```

Then in any new session, open with:

> "I am building an HR Analytics Chatbot. My GitHub repo is `<your-repo-url>`. Read `DEVLOG.md` for full context and continue from Day 3."

