# HR Analytics Chatbot — Development Log (Index)

## Session Rules (canonical)

See CODING-GUIDELINES.md.

## What this file is

This DEVLOG is an index + progress tracker. Reference material lives in:
ARCHITECTURE.md, DESIGN.md, CURRENT_TASK.md, CODING-GUIDELINES.md, DECISIONS.md.

## File Status (source of truth)

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
| backend/insights/generator.py | ⏳ Day 12-13 | — |
| backend/insights/related_questions.py | ⏳ Day 13 | — |
| backend/audit/audit_logger.py | ⏳ Day 13 | — |
| backend/routers/chat.py | ⏳ Day 15 | — |
| frontend/src/components/Login.tsx | ⏳ Day 16 | — |
| frontend/src/api/client.ts | ⏳ Day 16 | — |
| frontend/src/components/Chat.tsx | ⏳ Day 17 | — |
| frontend/src/components/Visualizations.tsx | ⏳ Day 18 | — |
| frontend/src/components/QuerySuggestions.tsx | ⏳ Day 18 | — |

## Completed Days

### Day 1 — Docker Scaffold ✅ COMPLETE

Milestone: docker-compose up → all 5 services green ✅

### Day 2 — Database Schema + Seed Data ✅ COMPLETE

Milestone: psql connects, RLS works, 500 employees seeded ✅

### Day 3 — Backend Core + JWT Auth ✅ COMPLETE

Milestone: POST /api/auth/login returns JWT for all 3 roles ✅

### Day 4 — Cube.js Semantic Layer ⏳ NEXT

See CURRENT_TASK.md.

## Resume Instructions

1. Read CURRENT_TASK.md + CODING-GUIDELINES.md first.
2. Pull ARCHITECTURE.md or DECISIONS.md only if the task needs it.
