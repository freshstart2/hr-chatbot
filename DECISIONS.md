# DECISIONS (Why things are the way they are)

| Decision | Reason |
|---|---|
| supervisor_id not manager_id | Matched Demographics-1.csv column naming |
| days_open removed from hiring_requisitions | CURRENT_DATE not immutable — cannot use in GENERATED ALWAYS AS |
| DO $$ IF NOT EXISTS $$ for CREATE ROLE | hr_admin is a built-in PostgreSQL 15 role |
| Frontend volumes: src/public/index/vite only | Windows node_modules overwrites container node_modules |
| RLS via current_setting('app.user_role') | Stateless per-request enforcement without separate DB users |
| bcrypt pinned to 4.0.1 | passlib==1.7.4 incompatible with bcrypt>=4.1.0 |
| Hashes pre-computed inside container | Windows bcrypt hashes incompatible with container bcrypt |
| bcrypt import removed from generate_seed.py | Hashes are hardcoded constants — no runtime hashing needed |
| admin@hr.com not hr_admin@hr.com | Exact email matches what seed inserts into hr.users |
| DATABASE_URL uses postgresql:// in .env | session.py replaces prefix with postgresql+asyncpg:// at runtime |
| NullPool for SQLAlchemy engine | Prevents connection pool issues with asyncpg in FastAPI |
| version removed from docker-compose.yml | Docker Compose v2 deprecated the version field |
