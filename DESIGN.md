# DESIGN — HR Analytics Chatbot

## Product Overview

A privacy-first, locally-hosted HR Analytics Chatbot where HR managers ask questions in natural language and get instant answers with charts, insights, and proactive anomaly detection.

## Roadmap

| Version | Goal | Timeline |
|---|---|---|
| v1.1 | POC — conversational chat, metric routing, RLS, visualizations | 6 weeks |
| v2.0 | Production — LangGraph, vLLM, Redis, differential privacy | +10 weeks |
| v2.5 | Proactive — Morning Brief, Why Engine, Scenario Sandbox | +8 weeks |
| v3.0 | Enterprise — GraphRAG, Flight Risk ML, Multi-tenancy | +16 weeks |

## Three User Personas

| Persona | Email | Role | Access |
|---|---|---|---|
| Analyst User | analyst@hr.com | analyst | Aggregates only, no PII, active employees only |
| Michael Manager | manager@hr.com | manager | Own team only (RLS: supervisor_id = user_id) |
| Admin Lisa | admin@hr.com | hr_admin | Full company, all tables |

## UX Intent

- Chat answers include charts, insight badges, and 3 follow-up suggestions.
- Strict privacy posture: RLS + suppression (e.g., analyst querying salary must be blocked).
- Empty state shows role-based hardcoded query suggestions.
- Export button: download result as CSV.

## Verified Endpoints (Day 3)

| Method | Endpoint | Status | Notes |
|---|---|---|---|
| GET | /health | 200 OK | Returns version + environment |
| POST | /api/auth/login | 200 OK | Returns JWT + role + name |
| POST | /api/chat | Placeholder | Echo only — Day 15 target |

## JWT Payload Structure

{
  "user_id": 1,
  "role": "hr_admin",
  "email": "admin@hr.com",
  "name": "Admin Lisa",
  "exp": "8 hours from issue"
}
