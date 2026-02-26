# ARCHITECTURE — HR Analytics Chatbot

## Goal

A privacy-first, locally-hosted HR Analytics Chatbot where HR managers ask questions in natural language and get answers with charts, insights, and anomaly detection.

## Non-negotiables

- 100% local — no cloud, no data egress
- Semantic layer: Cube.js (metric definitions + RLS enforcement)
- Database: PostgreSQL 15 with Row-Level Security
- Backend: FastAPI (Python 3.11)
- Frontend: React + Vite 5 + TypeScript + Recharts
- LLM: Ollama (llama3.2:3b pulling; llama3:8b target)

## Hardware & Environment

| Component | Detail |
|---|---|
| GPU | NVIDIA RTX 5060 Ti |
| VRAM | 16GB |
| CUDA | 13.1 |
| Driver | 591.86 |
| OS | Windows (Docker Desktop) |
| Docker GPU | Confirmed working |
| Project Path | C:\AIAgent\hr-chatbot\ |

## Docker Services

| Container | Image | Port | Status |
|---|---|---|---|
| hr_postgres | postgres:15-alpine | 5432 | Healthy |
| hr_ollama | ollama/ollama:latest | 11434 | Running (model pulling) |
| hr_cubejs | cubejs/cube:latest | 4000 | Day 4 |
| hr_backend | hr-chatbot-backend | 8000 | Running |
| hr_frontend | hr-chatbot-frontend | 3000 | Day 16 |

## Database Schema (hr schema)

### hr.employees (32 columns)

id, first_name, last_name, email,
gender, date_of_birth,
business_title, level,
primary_skill, secondary_skill,
employment_category, employment_type, employment_status,
work_mode, work_city, work_country, work_state,
start_date, termination_date, last_promotion_date, last_job_change_date,
supervisor_first_name, supervisor_last_name, supervisor_id (FK to employees.id),
department_l1, department_l2, department_l3,
hr_bp_name, job_project, job_client,
termination_reason, salary, created_at

### hr.employee_exits

id, employee_id (FK to employees.id), exit_date,
exit_type (voluntary|involuntary|retirement), reason, created_at

### hr.performance_reviews

id, employee_id (FK to employees.id), review_date,
rating (1.0-5.0), reviewer_id (FK to employees.id), created_at

### hr.hiring_requisitions

id, department, open_date, close_date,
status (open|filled|cancelled), created_at

days_open is NOT a column — compute as:
COALESCE(close_date, CURRENT_DATE) - open_date

### hr.users

user_id, name, email, hashed_password,
role (analyst|manager|hr_admin),
employee_id (FK to employees.id, nullable), created_at

### hr.query_audit_log

id, user_id (FK to users.user_id), role,
query_text, resolved_query, metric_id,
execution_type (metric_route|llm_generated),
execution_ms, cache_hit, session_id, turn_number, created_at

### hr.conversation_sessions

session_id (PK, VARCHAR), user_id (FK to users.user_id),
turns (JSONB default '[]'), created_at, updated_at

## RLS Policies

### hr.employees

- hr_admin: ALL rows
- manager: supervisor_id = app.user_id only
- analyst: Active employees only

### hr.performance_reviews

- hr_admin: ALL reviews
- manager: direct reports only
- analyst: ALL reviews

### Session variables (set per request in backend)

SET app.user_role = 'manager';
SET app.user_id   = '3';

## Seed Data (verified)

- Total employees: 500
- Active: 310, Inactive: 190
- employee_exits: 190 (matches inactive exactly)
- performance_reviews: 700 (350 employees x 2 cycles)
- hiring_requisitions: 25
- Departments: Engineering(114), Product Development(90), Analytics(77), Sales(77), Marketing(47), Finance(35), Human Resource(31), Business analyst(29)
- App users:
  - analyst@hr.com / analyst123 / analyst
  - manager@hr.com / manager123 / manager
  - admin@hr.com / admin123 / hr_admin

NOTE: Email is admin@hr.com — NOT hr_admin@hr.com

## .env Variables (structure only — no values)

POSTGRES_DB=hr_analytics
POSTGRES_USER=hr_admin
POSTGRES_PASSWORD=secret
CUBEJS_DB_TYPE=postgres
CUBEJS_DB_HOST=postgres
CUBEJS_DB_NAME=hr_analytics
CUBEJS_DB_USER=hr_admin
CUBEJS_DB_PASS=secret
CUBEJS_API_SECRET=secret
OLLAMA_BASE_URL=http://hr_ollama:11434
OLLAMA_MODEL=llama3.2:3b
JWT_SECRET=secret
JWT_ALGORITHM=HS256
JWT_EXPIRY_HOURS=8
ENVIRONMENT=development
LOG_LEVEL=info

## 9-Layer Chat Pipeline (Day 15 target)

1. JWT decode - user_id, role
2. Conversation fetch - last 5 turns from memory
3. Policy guardrails - block forbidden keywords
4. Reference resolver - rewrite follow-ups as standalone queries
5a. Metric routing - match pre-built metric (fast path under 100ms)
5b. LLM generation - generate Cube.js query spec (fallback), then spec validation
6. Cube.js execution - run query, get raw data
7. Visualization - detect chart type, build config
8. Insight generation - YoY comparison, benchmarks
9. Audit log + Conversation store + Return response
