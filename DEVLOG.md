<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

```markdown
# HR Analytics Chatbot — Development Log

---

## Session Rules (apply to ALL sessions on this project)

- Complete file code only — no snippets, no partial blocks
- Never assume things not in context — ask first
- Audit before generating — cross-check all column/table/role names
- Every file change = immediate git add + git commit before moving to next task
- One file at a time — wait for confirmation before next file

---

## Product Overview

A **privacy-first, locally-hosted HR Analytics Chatbot** where HR managers ask
questions in natural language ("What is our attrition rate in Engineering?") and
get instant answers with charts, insights, and proactive anomaly detection.

- 100% local — no cloud, no data egress
- LLM: Llama-3 8B via Ollama (RTX 5060 Ti GPU)
- Semantic Layer: Cube.js (metric definitions + RLS enforcement)
- Database: PostgreSQL 15 with Row-Level Security
- Backend: FastAPI (Python 3.11)
- Frontend: React + Vite 5 + Recharts
- Orchestration: Docker Compose (v1.1), LangGraph added in v2.0

### Version Roadmap

| Version | Goal | Timeline |
|---------|------|----------|
| v1.1 | POC — conversational chat, metric routing, RLS, visualizations | 6 weeks |
| v2.0 | Production — LangGraph, vLLM, Redis, differential privacy | +10 weeks |
| v2.5 | Proactive — Morning Brief, "Why" Engine, Scenario Sandbox | +8 weeks |
| v3.0 | Enterprise — GraphRAG, Flight Risk ML, Multi-tenancy | +16 weeks |

---

## Hardware & Environment

| Component | Detail |
|-----------|--------|
| GPU | NVIDIA RTX 5060 Ti |
| VRAM | 16GB |
| CUDA | 13.1 |
| Driver | 591.86 |
| OS | Windows (Docker Desktop) |
| Docker GPU | ✅ Confirmed working |
| Project Path | C:\AIAgent\hr-chatbot\ |

---

## Tech Stack (Locked)

| Layer | Technology | Notes |
|-------|-----------|-------|
| Frontend | React + Vite 5.4.2 + TypeScript | NOT Vite 6 — rolldown Docker bug |
| Frontend Node | node:22-slim | NOT alpine — musl breaks rolldown bindings |
| Charts | Recharts | Proven in hr-dashboard prototype |
| Backend | FastAPI (Python 3.11) | python:3.11-slim |
| LLM | Ollama llama3.2:3b (pulling) | llama3:8b target when available |
| Metrics | Cube.js latest stable | Full pre-aggregation support |
| Database | PostgreSQL 15 (Alpine) | |
| Auth | JWT HS256 | Upgrade to RS256 in v2.0 |
| Deployment | Docker Compose | Windows host |
| Embeddings | all-MiniLM-L6-v2 (SBERT) | sentence-transformers in requirements |

---

## Docker Services

| Container | Image | Port | Status |
|-----------|-------|------|--------|
| hr_postgres | postgres:15-alpine | 5432 | ✅ Healthy |
| hr_ollama | ollama/ollama:latest | 11434 | ✅ Running (model pulling) |
| hr_cubejs | cubejs/cube:latest | 4000 | ⏳ Day 4 |
| hr_backend | hr-chatbot-backend | 8000 | ✅ Running |
| hr_frontend | hr-chatbot-frontend | 3000 | ⏳ Day 16 |

### Critical Docker Notes

- Frontend base image MUST be node:22-slim — NOT node:22-alpine (musl rolldown bug)
- Vite MUST be pinned to ^5.4.2 — Vite 6 rolldown optional deps bug in Docker
- node_modules must NOT be mounted from Windows host
- PostgreSQL init scripts only run on FIRST container start — use docker-compose down -v to reset
- bcrypt hashes must be generated INSIDE the backend container — Windows hashes are incompatible

### Frontend Volume Strategy

```yaml
volumes:
  - ./frontend/src:/app/src
  - ./frontend/public:/app/public
  - ./frontend/index.html:/app/index.html
  - ./frontend/vite.config.ts:/app/vite.config.ts
  # node_modules stays INSIDE container — never mount from Windows
```


---

## Project Structure

```
C:\AIAgent\hr-chatbot\
├── docker-compose.yml
├── DEVLOG.md
├── .env                              ← never commit
├── .gitignore
├── infrastructure/
│   └── db/
│       ├── schema.sql                ← 01_schema
│       ├── rls_policies.sql          ← 02_rls
│       ├── seed_data.sql             ← 03_seed (generated — never commit)
│       └── generate_seed.py         ← run on Windows host
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py
│   │   └── models.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── jwt_handler.py
│   │   └── dependencies.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── auth.py                  ← Day 3 ✅
│   ├── llm/
│   │   ├── __init__.py
│   │   └── client.py                ← Day 3 ✅
│   ├── metrics/                     ← Day 6-7
│   │   ├── __init__.py
│   │   ├── metrics.yaml
│   │   └── metric_registry.py
│   ├── cube/                        ← Day 4
│   │   ├── __init__.py
│   │   └── cube_api_client.py
│   ├── conversation/                ← Day 10
│   │   ├── __init__.py
│   │   ├── manager.py
│   │   └── reference_resolver.py
│   ├── visualization/               ← Day 11
│   │   ├── __init__.py
│   │   └── engine.py
│   ├── insights/                    ← Day 12-13
│   │   ├── __init__.py
│   │   ├── generator.py
│   │   └── related_questions.py
│   ├── audit/                       ← Day 13
│   │   ├── __init__.py
│   │   └── audit_logger.py
│   └── security/                    ← Week 5
│       └── __init__.py
├── cube/
│   └── schema/                      ← Day 4
│       ├── Employee.js
│       ├── EmployeeAggregates.js
│       └── HiringRequisitions.js
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── vite.config.ts
    ├── index.html
    ├── src/
    │   ├── components/
    │   │   ├── Login.tsx             ← Day 16
    │   │   ├── Chat.tsx              ← Day 17
    │   │   ├── Visualizations.tsx    ← Day 18
    │   │   └── QuerySuggestions.tsx  ← Day 18
    │   └── api/
    │       └── client.ts             ← Day 16
    └── public/
```


---

## File Status

| File | Status | Day |
| :-- | :-- | :-- |
| docker-compose.yml | ✅ Complete | Day 1 |
| .env | ✅ Complete | Day 1 |
| .gitignore | ✅ Complete | Day 1 |
| infrastructure/db/schema.sql | ✅ Complete | Day 2 |
| infrastructure/db/rls_policies.sql | ✅ Complete | Day 2 |
| infrastructure/db/generate_seed.py | ✅ Complete | Day 3 |
| infrastructure/db/seed_data.sql | ✅ Generated | Day 2 |
| backend/Dockerfile | ✅ Complete | Day 1 |
| backend/requirements.txt | ✅ Complete | Day 3 |
| backend/main.py | ✅ Complete | Day 3 |
| backend/core/config.py | ✅ Complete | Day 3 |
| backend/db/session.py | ✅ Complete | Day 3 |
| backend/db/models.py | ✅ Complete | Day 3 |
| backend/auth/jwt_handler.py | ✅ Complete | Day 3 |
| backend/auth/dependencies.py | ✅ Complete | Day 3 |
| backend/routers/auth.py | ✅ Complete | Day 3 |
| backend/llm/client.py | ✅ Complete | Day 3 |
| cube/schema/Employee.js | ⏳ Day 4 | — |
| cube/schema/EmployeeAggregates.js | ⏳ Day 4 | — |
| cube/schema/HiringRequisitions.js | ⏳ Day 4 | — |
| backend/cube/cube_api_client.py | ⏳ Day 4 | — |
| backend/metrics/metrics.yaml | ⏳ Day 6 | — |
| backend/metrics/metric_registry.py | ⏳ Day 6 | — |
| backend/llm/prompt_builder.py | ⏳ Day 8 | — |
| backend/llm/spec_validator.py | ⏳ Day 8 | — |
| backend/conversation/manager.py | ⏳ Day 10 | — |
| backend/conversation/reference_resolver.py | ⏳ Day 10 | — |
| backend/visualization/engine.py | ⏳ Day 11 | — |
| backend/insights/generator.py | ⏳ Day 12 | — |
| backend/insights/related_questions.py | ⏳ Day 13 | — |
| backend/audit/audit_logger.py | ⏳ Day 13 | — |
| backend/routers/chat.py | ⏳ Day 15 | — |
| frontend/src/components/Login.tsx | ⏳ Day 16 | — |
| frontend/src/api/client.ts | ⏳ Day 16 | — |
| frontend/src/components/Chat.tsx | ⏳ Day 17 | — |
| frontend/src/components/Visualizations.tsx | ⏳ Day 18 | — |
| frontend/src/components/QuerySuggestions.tsx | ⏳ Day 18 | — |


---

## Database Schema — All 7 Tables (hr schema)

### hr.employees (32 columns)

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
id, employee_id (FK → employees.id), exit_date,
exit_type (voluntary|involuntary|retirement), reason, created_at
```


### hr.performance_reviews

```
id, employee_id (FK → employees.id), review_date,
rating (1.0–5.0), reviewer_id (FK → employees.id), created_at
```


### hr.hiring_requisitions

```
id, department, open_date, close_date,
status (open|filled|cancelled), created_at
NOTE: days_open NOT a column — compute as:
      COALESCE(close_date, CURRENT_DATE) - open_date
```


### hr.users

```
user_id, name, email, hashed_password,
role (analyst|manager|hr_admin),
employee_id (FK → employees.id, nullable), created_at
```


### hr.query_audit_log

```
id, user_id (FK → users.user_id), role,
query_text, resolved_query, metric_id,
execution_type (metric_route|llm_generated),
execution_ms, cache_hit, session_id, turn_number, created_at
```


### hr.conversation_sessions

```
session_id (PK, VARCHAR), user_id (FK → users.user_id),
turns (JSONB default '[]'), created_at, updated_at
```


---

## Seed Data — Verified State

```
Total employees:    500
Active:             310
Inactive:           190
employee_exits:     190 (matches Inactive exactly)
performance_reviews: 700 (350 employees × 2 review cycles)
hiring_requisitions: 25
Departments:        Engineering(114), Product Development(90),
                    Analytics(77), Sales(77), Marketing(47),
                    Finance(35), Human Resource(31), Business analyst(29)
App users:
  analyst@hr.com  / password: analyst123 / role: analyst
  manager@hr.com  / password: manager123 / role: manager
  admin@hr.com    / password: admin123   / role: hr_admin
```

NOTE: Email is admin@hr.com — NOT hr_admin@hr.com

---

## RLS Policies

### hr.employees

- hr_admin → ALL rows
- manager → supervisor_id = app.user_id only
- analyst → Active employees only


### hr.performance_reviews

- hr_admin → ALL reviews
- manager → direct reports only
- analyst → ALL reviews


### Session variables (set per request in backend)

```sql
SET app.user_role = 'manager';
SET app.user_id   = '3';
```


---

## Three User Personas

| Persona | Email | Role | Access |
| :-- | :-- | :-- | :-- |
| Analyst User | analyst@hr.com | analyst | Aggregates only, no PII, active employees only |
| Michael Manager | manager@hr.com | manager | Own team only (RLS: supervisor_id = user_id) |
| Admin Lisa | admin@hr.com | hr_admin | Full company, all tables |


---

## Verified Endpoints (Day 3)

| Method | Endpoint | Status | Notes |
| :-- | :-- | :-- | :-- |
| GET | /health | ✅ 200 | Returns version + environment |
| POST | /api/auth/login | ✅ 200 | Returns JWT + role + name |
| POST | /api/chat | ⏳ Placeholder | Echo only — Day 15 target |

### JWT Payload

```json
{
  "user_id": 1,
  "role": "hr_admin",
  "email": "admin@hr.com",
  "name": "Admin Lisa",
  "exp": "<8 hours from issue>"
}
```


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
OLLAMA_MODEL=llama3.2:3b
JWT_SECRET=<secret>
JWT_ALGORITHM=HS256
JWT_EXPIRY_HOURS=8
ENVIRONMENT=development
LOG_LEVEL=info
```


---

## 9-Layer Chat Pipeline (Day 15 target)

```
1.  JWT decode          → user_id, role
2.  Conversation fetch  → last 5 turns from memory
3.  Policy guardrails   → block forbidden keywords
4.  Reference resolver  → rewrite follow-ups as standalone queries
5a. Metric routing      → match to pre-built metric (fast path <100ms)
5b. LLM generation      → generate Cube.js query spec (fallback)
    Spec validation     → validate against schema + RLS
6.  Cube.js execution   → run query, get raw data
7.  Visualization       → detect chart type, build config
8.  Insight generation  → YoY comparison, benchmarks
9.  Audit log           → write full record to DB
    Conversation store  → append turn
    Return              → answer + chart_config + insights + suggestions
```


---

## 6-Week Build Plan

### Week 1: Foundation (Days 1–5)

#### Day 1 — Docker Scaffold ✅ COMPLETE

Goal: All 5 services start with docker-compose up

- [x] Git repo + folder structure
- [x] docker-compose.yml (5 services)
- [x] .env file
- [x] .gitignore
- [x] GPU confirmed in Docker (RTX 5060 Ti, CUDA 13.1)
- [x] Frontend Dockerfile (node:22-slim, Vite 5.4.2)
- [x] Backend Dockerfile + placeholder main.py
- [x] Cube.js placeholder schema

Milestone: docker-compose up → all 5 services green ✅

#### Day 2 — Database Schema + Seed Data ✅ COMPLETE

Goal: PostgreSQL with HR data, RLS policies, audit tables

- [x] infrastructure/db/schema.sql (7 tables, 18 indexes)
- [x] infrastructure/db/rls_policies.sql (RLS on employees + reviews)
- [x] infrastructure/db/generate_seed.py (500 employees, Faker)
- [x] infrastructure/db/seed_data.sql (generated)
- [x] Verified: 500 employees, 310 active, 190 inactive, 190 exits

Milestone: psql connects, RLS works, 500 employees seeded ✅

#### Day 3 — Backend Core + JWT Auth ✅ COMPLETE

Goal: Backend running, login endpoint working, Ollama client ready

- [x] backend/requirements.txt (sqlalchemy, bcrypt==4.0.1 pinned)
- [x] backend/core/config.py (pydantic-settings)
- [x] backend/db/session.py (asyncpg, NullPool)
- [x] backend/db/models.py (all 7 ORM models)
- [x] backend/auth/jwt_handler.py (HS256, 8hr expiry)
- [x] backend/auth/dependencies.py (get_current_user)
- [x] backend/routers/auth.py (POST /api/auth/login)
- [x] backend/llm/client.py (generate + chat, 3 retries)
- [x] backend/main.py (CORS, lifespan, routers)
- [x] Verified: login works for all 3 users

Milestone: POST /api/auth/login returns JWT for all 3 roles ✅

#### Day 4 — Cube.js Semantic Layer ⏳ NEXT

Goal: 5 core metrics queryable via Cube.js API with RLS

Files to create:

- cube/schema/Employee.js
    - sql → hr.employees
    - Measures: count (headcount), activeCount, inactiveCount
    - Dimensions: department_l1, level, gender, work_mode, work_city,
employment_type, employment_status
    - RLS via queryRewrite using securityContext.role and securityContext.userId
- cube/schema/EmployeeAggregates.js
    - Attrition rate (exits / headcount)
    - Average tenure (CURRENT_DATE - start_date in months)
    - Average performance rating (from performance_reviews)
    - Pre-aggregations partitioned by department
- cube/schema/HiringRequisitions.js
    - Open reqs count
    - Time to fill (COALESCE(close_date, CURRENT_DATE) - open_date)
    - Status breakdown
- backend/cube/cube_api_client.py
    - execute_query(query_spec, security_context) async method
    - Passes JWT context for RLS enforcement
    - Returns normalized data list

Before starting Day 4, provide:

1. docker-compose logs cubejs
2. docker exec -it hr_ollama ollama list

Milestone: 5 metrics queryable in Cube.js Playground (port 4000) ✅

#### Day 5 — Modelfile + LLM Verification ⏳

Goal: Ollama responding with structured JSON output

Files to create:

- backend/llm/modelfile
    - System prompt: JSON-only Cube.js spec output
    - Temperature: 0.1
    - Context window: 4096
- Manual test: send HR query, confirm JSON response structure

Milestone: Backend calls Ollama, receives valid JSON ✅

---

### Week 2: Core Chat Pipeline (Days 6–10)

#### Days 6–7 — Metrics Registry + Routing

Goal: 15 metrics defined, 60% of queries take fast path

Files to create:

- backend/metrics/metrics.yaml
    - 15 metrics: headcount (total, by dept, by location), attrition rate
(overall, by dept), avg tenure (overall, by dept), avg performance rating,
headcount by job level, voluntary exits this quarter,
open requisitions count, time to fill
    - Each metric: id, description, synonyms[], cube_query_spec, allowed_roles[]
- backend/metrics/metric_registry.py
    - Load metrics.yaml on startup
    - Build SBERT embedding index (all-MiniLM-L6-v2)
    - find_metric(query_text) → best match + confidence score
    - Confidence threshold: 0.80 (below = LLM fallback)

Test queries that must route correctly:
"how many employees do we have" → total_headcount
"show attrition by department" → attrition_by_department
"what is our workforce composition" → headcount_by_level

Milestone: 10/10 test queries routed correctly ✅

#### Days 8–9 — LLM Chain + Query Spec Validator

Goal: Complex queries generate valid Cube.js specs

Files to create:

- backend/llm/prompt_builder.py
    - System prompt embeds Cube.js schema + available dimensions + user role
    - Few-shot examples: query → JSON spec
    - Output format: {measures[], dimensions[], filters[], timeDimensions[]}
- backend/llm/spec_validator.py
    - Validate JSON spec against Cube.js schema
    - Check measures/dimensions exist in registry
    - Check user role can access all requested measures
    - Return list of validation errors

Milestone: Complex query → valid spec → correct Cube.js result ✅

#### Day 10 — Conversation Memory + Reference Resolver

Goal: Follow-up questions understood correctly

Files to create:

- backend/conversation/manager.py
    - In-memory store: {user_id: {session_id: [ConversationTurn]}}
    - create_session(user_id) → session_id
    - get_history(user_id, session_id, max_turns=5) → list
    - add_turn(user_id, session_id, turn) → void
    - 30-minute TTL, session ownership verification
- backend/conversation/reference_resolver.py
    - Detect patterns: "what about", "and for", "same for", "just", "last year"
    - If detected + history exists → LLM rewrites as standalone query
    - If no history → return original unchanged

Test 3-turn flow:
"What's our headcount?" → 500
"What about Engineering?" → resolved → 114
"And last year?" → resolved → Engineering headcount last year

Milestone: 3-turn conversation works end-to-end ✅

---

### Week 3: UX Features (Days 11–15)

#### Days 11–12 — Visualization Engine + Insights

Goal: Queries return chart config + YoY insights

Files to create:

- backend/visualization/engine.py
    - No dimensions + 1 row → single_value
    - Time dimension → line_chart
    - 1 dimension + ≤10 rows → bar_chart
    - 2 dimensions → heatmap
    - Default → table
    - Returns frontend-ready chart config (labels, datasets, type)
- backend/insights/generator.py
    - Fetch same metric from 1 year prior
    - Compute YoY % change
    - Fetch industry benchmarks from config file
    - Return 2-3 insight objects with direction (positive/negative/neutral)

Milestone: Attrition query returns chart config + YoY insight ✅

#### Days 13–14 — Related Questions + Audit Logging

Goal: Every query logged, follow-up suggestions generated

Files to create:

- backend/insights/related_questions.py
    - LLM prompt: given query + result → suggest 3 follow-up questions
    - Cache suggestions by metric_id
    - Return as list of strings
- backend/audit/audit_logger.py
    - Write to query_audit_log after every request
    - Fields: user_id, role, query_text, resolved_query, metric_id,
execution_type, execution_ms, cache_hit, session_id, turn_number

Milestone: Every query logged, 3 suggestions returned ✅

#### Day 15 — Wire /api/chat Pipeline

Goal: Single endpoint handles complete 9-layer query lifecycle

Files to create/complete:

- backend/routers/chat.py
    - POST /api/chat — requires JWT
    - Accepts: {text, session_id}
    - Executes all 9 pipeline layers in order
    - Returns: {answer, chart_config, insights, suggestions, session_id}

Milestone: End-to-end chat query works for all 3 roles ✅

---

### Week 4: Frontend (Days 16–20)

#### Days 16–17 — Auth + Chat UI

Goal: Login works, chat interface renders messages

Files to create:

- frontend/src/api/client.ts
    - Axios client with JWT header injection
    - POST /api/auth/login → store token in memory (NOT localStorage)
    - POST /api/chat → send message + session_id
- frontend/src/components/Login.tsx
    - Email + password form
    - On success → redirect to chat
    - On failure → show error
- frontend/src/components/Chat.tsx
    - Message history (user + bot bubbles)
    - Streaming response loader
    - Empty state with role-based query suggestions (hardcoded per role)
    - Input box with submit on Enter

Milestone: Login → chat → first response visible ✅

#### Days 18–19 — Visualizations + Insights Display

Goal: Charts render, insights show, suggestions clickable

Files to create:

- frontend/src/components/Visualizations.tsx
    - Consume chart_config from API response
    - Render via Recharts (BarChart, LineChart, single value card)
- frontend/src/components/InsightBadges.tsx
    - Colored chips: green (positive), yellow (neutral), red (negative)
    - Render below answer text
- frontend/src/components/QuerySuggestions.tsx
    - Clickable chips from suggestions[]
    - Auto-submit on click
- Export button: download result as CSV

Milestone: Attrition query shows bar chart + insight badge ✅

#### Day 20 — Query History + Polish

Goal: Session history visible, error states handled

Changes:

- Sidebar: last 20 queries from session (click to re-run)
- "View in Dashboard →" link for metric-routed queries
- Error states: privacy suppression, timeout, empty result, 401

Milestone: Complete UI polished, all error states handled ✅

---

### Weeks 5–6: Testing + Security Hardening

#### Security Tests (Non-Negotiable)

| Test | Expected Result |
| :-- | :-- |
| Analyst queries raw employees table | 403 blocked by RLS |
| Manager queries another manager's team | Returns only own team |
| Session A reads Session B's history | Returns empty (ownership check) |
| SQL injection in query text | Parameterized query — no effect |
| JWT with tampered role field | Signature verification fails |
| Analyst queries individual salary | Suppression triggered |

#### Performance Tests

- 5 concurrent users → P95 latency <2 seconds
- 30+ metric routing queries → all <100ms
- LLM queue: 3 queued requests → all served in order


#### Pilot Preparation

- Load realistic seed data (500+ employees) — ✅ Done
- Create accounts for 8-10 pilot users
- Write user guide (1 page: what you can ask, examples)
- Set up basic Prometheus + Grafana dashboard
- Create on-call runbook for common issues

---

## Key Decisions Made

| Decision | Reason |
| :-- | :-- |
| supervisor_id not manager_id | Matched Demographics-1.csv column naming |
| days_open removed from hiring_requisitions | CURRENT_DATE not immutable — cannot use in GENERATED ALWAYS AS |
| DO \$ IF NOT EXISTS \$ for CREATE ROLE | hr_admin is a built-in PostgreSQL 15 role |
| Frontend volumes: src/public/index/vite only | Windows node_modules overwrites container node_modules |
| RLS via current_setting('app.user_role') | Stateless per-request enforcement without separate DB users |
| bcrypt pinned to 4.0.1 | passlib==1.7.4 incompatible with bcrypt>=4.1.0 |
| Hashes pre-computed inside container | Windows bcrypt hashes incompatible with container bcrypt |
| bcrypt import removed from generate_seed.py | Hashes are hardcoded constants — no runtime hashing needed |
| admin@hr.com not hr_admin@hr.com | Exact email matches what seed inserts into hr.users |
| DATABASE_URL uses postgresql:// in .env | session.py replaces prefix with postgresql+asyncpg:// at runtime |
| NullPool for SQLAlchemy engine | Prevents connection pool issues with asyncpg in FastAPI |
| version removed from docker-compose.yml | Docker Compose v2 deprecated the version field |


---

## Known Issues \& Solutions

| Issue | Solution |
| :-- | :-- |
| Vite 6 rolldown native binding error in Docker | Pin Vite to ^5.4.2 in package.json |
| node:22-alpine rolldown musl binding error | Use node:22-slim (Debian-based) |
| Windows node_modules mounted into Linux container | Mount only src/, public/ — never node_modules |
| PowerShell curl syntax differs from bash | Use Invoke-WebRequest with @{} header syntax |
| PostgreSQL init scripts not running | Scripts only run on FIRST start — docker-compose down -v to reset |
| bcrypt version mismatch host vs container | Always generate hashes inside hr_backend container |
| hr_admin is a built-in PostgreSQL 15 role | Use DO \$ IF NOT EXISTS \$ block |
| GENERATED ALWAYS AS with CURRENT_DATE fails | Remove days_open column — compute in queries instead |
| docker rmi fails — image in use | docker rm {container_id} first, then docker rmi |


---

## Useful Commands

```cmd
# Start everything
cd C:\AIAgent\hr-chatbot
docker-compose up -d

# Watch logs
docker-compose logs -f backend
docker-compose logs -f postgres

# Full rebuild after requirements change
docker-compose build --no-cache backend
docker-compose up -d backend

# Shell inside container
docker exec -it hr_backend bash
docker exec -it hr_postgres psql -U hr_admin -d hr_analytics

# Nuclear reset (DELETES DATABASE)
docker-compose down -v

# Regenerate bcrypt hashes inside container
docker exec -it hr_backend python -c "
from passlib.context import CryptContext
ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')
print('analyst:', ctx.hash('analyst123'))
print('manager:', ctx.hash('manager123'))
print('admin:', ctx.hash('admin123'))
"
```


## How to Regenerate Seed Data (after docker-compose down -v)

```cmd
python infrastructure/db/generate_seed.py
docker-compose down -v
docker-compose up -d
docker-compose logs -f postgres
```


---

## How to Resume in a New Session

1. Provide the GitHub repo URL
2. Say: "Read DEVLOG.md and continue. Session rules apply immediately."
3. New session must read this file before generating any code
4. Check File Status table for current state
5. Check the current day's section for exact files to build next
```

***

## Git Commands

```cmd
cd C:\AIAgent\hr-chatbot
git add DEVLOG.md
git commit -m "docs: complete DEVLOG with full 6-week plan, all days detailed"
git push origin main
```

Then share the two Day 4 prerequisites:

```cmd
docker-compose logs cubejs
docker exec -it hr_ollama ollama list
```

<span style="display:none">[^1][^2]</span>

<div align="center">⁂</div>

[^1]: V1.1-Implementation-Kickoff.md

[^2]: HR_CHATBOT_SESSION_STATE.md

