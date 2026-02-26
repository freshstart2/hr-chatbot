# CODING GUIDELINES (Project Rules)

## Session Rules (apply to ALL sessions)

- Complete file code only — no snippets, no partial blocks
- Never assume things not in context — ask first
- Audit before generating — cross-check all column/table/role names against ARCHITECTURE.md
- Every file change = immediate git add + git commit before moving to next task
- One file at a time — wait for confirmation before next file

## Tech Stack (Locked)

| Layer | Technology | Notes |
|---|---|---|
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

## Docker and Frontend Volume Rules

- Frontend base image MUST be node:22-slim — NOT node:22-alpine (musl rolldown bug)
- Vite MUST be pinned to ^5.4.2 — Vite 6 rolldown optional deps bug in Docker
- node_modules must NOT be mounted from Windows host

Correct volume mounts:
  - ./frontend/src to /app/src
  - ./frontend/public to /app/public
  - ./frontend/index.html to /app/index.html
  - ./frontend/vite.config.ts to /app/vite.config.ts
  - node_modules stays INSIDE container — never mount from Windows

## Database and Auth Rules

- PostgreSQL init scripts only run on FIRST container start — use docker-compose down -v to reset
- bcrypt hashes must be generated INSIDE the backend container — Windows hashes are incompatible
- bcrypt pinned to 4.0.1 — passlib==1.7.4 incompatible with bcrypt>=4.1.0
- DATABASE_URL in .env uses postgresql:// — session.py replaces with postgresql+asyncpg:// at runtime
- NullPool for SQLAlchemy engine — prevents asyncpg pool issues in FastAPI

## Known Issues and Solutions

| Issue | Solution |
|---|---|
| Vite 6 rolldown native binding error in Docker | Pin Vite to ^5.4.2 in package.json |
| node:22-alpine rolldown musl binding error | Use node:22-slim (Debian-based) |
| Windows node_modules mounted into Linux container | Mount only src/, public/ — never node_modules |
| PowerShell curl syntax differs from bash | Use Invoke-WebRequest with @{} header syntax |
| PostgreSQL init scripts not running | Scripts only run on FIRST start — docker-compose down -v to reset |
| bcrypt version mismatch host vs container | Always generate hashes inside hr_backend container |
| hr_admin is a built-in PostgreSQL 15 role | Use DO $$ IF NOT EXISTS $$ block |
| GENERATED ALWAYS AS with CURRENT_DATE fails | Remove days_open column — compute in queries instead |
| docker rmi fails — image in use | docker rm container_id first, then docker rmi |

## Useful Commands

Start everything:
  cd C:\AIAgent\hr-chatbot
  docker-compose up -d

Watch logs:
  docker-compose logs -f backend
  docker-compose logs -f cubejs

Full rebuild after requirements change:
  docker-compose build --no-cache backend
  docker-compose up -d backend

Shell inside container:
  docker exec -it hr_backend bash
  docker exec -it hr_postgres psql -U hr_admin -d hr_analytics

Nuclear reset (DELETES DATABASE):
  docker-compose down -v

Regenerate bcrypt hashes inside container:
  docker exec -it hr_backend python -c "
  from passlib.context import CryptContext
  ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')
  print('analyst:', ctx.hash('analyst123'))
  print('manager:', ctx.hash('manager123'))
  print('admin:', ctx.hash('admin123'))
  "
