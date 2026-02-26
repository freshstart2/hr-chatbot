# CURRENT TASK — Day 4 (Cube.js Schema)

## Goal

5 core metrics queryable via Cube.js API with RLS.

## Prerequisites (must provide before coding)

1. docker-compose logs cubejs
2. docker exec -it hr_ollama ollama list

## Files to create (in order, one at a time)

### cube/schema/Employee.js

- sql: hr.employees
- Measures: count (headcount), activeCount, inactiveCount
- Dimensions: department_l1, level, gender, work_mode, work_city, employment_type, employment_status
- RLS via queryRewrite using securityContext.role and securityContext.userId

### cube/schema/EmployeeAggregates.js

- Attrition rate (exits / headcount)
- Average tenure (CURRENT_DATE - start_date in months)
- Average performance rating (from performance_reviews)
- Pre-aggregations partitioned by department

### cube/schema/HiringRequisitions.js

- Open reqs count
- Time to fill: COALESCE(close_date, CURRENT_DATE) - open_date
- Status breakdown

### backend/cube/cube_api_client.py

- execute_query(query_spec, security_context) async method
- Passes JWT context for RLS enforcement
- Returns normalized data list

## Milestone

5 metrics queryable in Cube.js Playground (port 4000).
