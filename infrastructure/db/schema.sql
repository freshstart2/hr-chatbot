-- ============================================================
-- HR Analytics Chatbot — Complete Database Schema
-- File: infrastructure/db/schema.sql
-- Run order: 01 (before rls_policies.sql and seed_data.sql)
-- ============================================================

CREATE SCHEMA IF NOT EXISTS hr;

-- ============================================================
-- CORE TABLE: employees
-- Aligned with Demographics-1.csv (all 30 original columns)
-- + salary column added for chatbot metric queries
-- ============================================================

CREATE TABLE hr.employees (
    id                      SERIAL PRIMARY KEY,

    -- Name (split from CSV: first_name + last_name)
    first_name              VARCHAR(100) NOT NULL,
    last_name               VARCHAR(100) NOT NULL,
    email                   VARCHAR(150) UNIQUE NOT NULL,

    -- Demographics (CSV: gender, Date of Birth)
    gender                  VARCHAR(30),
    date_of_birth           DATE,

    -- Role (CSV: Business Title, Level)
    business_title          VARCHAR(150),
    level                   VARCHAR(30),
    -- Level values: Associate | Professional | Senior Associate | Team Lead
    --               Manager | Senior Manager | Director | Senior Director | VP | SVP

    -- Skills (CSV: Primary Skill, Secondary Skill)
    primary_skill           VARCHAR(100),
    secondary_skill         VARCHAR(100),

    -- Employment classification (CSV: Employment Category, Employment Type, Employment Status)
    employment_category     VARCHAR(20),
    -- Values: Regular | Contractor | Intern
    employment_type         VARCHAR(20),
    -- Values: Full time | Part time
    employment_status       VARCHAR(20) NOT NULL DEFAULT 'Active',
    -- Values: Active | Inactive

    -- Location (CSV: Work Mode, Work City, Work Country, Work State)
    work_mode               VARCHAR(20),
    -- Values: Hybrid | Onsite | Remote
    work_city               VARCHAR(100),
    work_country            VARCHAR(100),
    work_state              VARCHAR(100),

    -- Dates (CSV: Start Date, Termination Date, Last Promotion Date, Last Job Change Date)
    start_date              DATE NOT NULL,
    termination_date        DATE,
    last_promotion_date     DATE,
    last_job_change_date    DATE,

    -- Supervisor (CSV: Supervisor First Name, Supervisor Last Name)
    supervisor_first_name   VARCHAR(100),
    supervisor_last_name    VARCHAR(100),
    supervisor_id           INT REFERENCES hr.employees(id),

    -- Org hierarchy (CSV: Department Level 1, Department Level 2, Department Level 3)
    department_l1           VARCHAR(100),
    -- Values: Engineering | Analytics | Sales | Product Development
    --         Finance | Marketing | Human Resource | Business analyst
    department_l2           VARCHAR(100),
    department_l3           VARCHAR(100),

    -- HR metadata (CSV: HR Business Partner Name, Job Project, Job Client)
    hr_bp_name              VARCHAR(150),
    job_project             VARCHAR(150),
    job_client              VARCHAR(150),

    -- Exit data (CSV: Termination Reason)
    termination_reason      VARCHAR(200),
    -- Values: Voluntary - Dissatisfied by Compensation | Voluntary - Dissatisfied by Manager
    --         Voluntary - Better Opportunity | Voluntary - Personal Reasons
    --         Voluntary - Return to School | Voluntary - Career Development
    --         Voluntary - Career Change | Voluntary - Relocation
    --         Voluntary - Health Reasons | Voluntary - Dissatisfied by Work Conditions
    --         Involuntary - Reduction in Force | Involuntary - Misconduct
    --         Involuntary - Unsatisfactory Performance | Involuntary - Mutual Consent

    -- Added for chatbot metric queries (not in original CSV)
    salary                  NUMERIC(10, 2),

    created_at              TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- SUPPORTING TABLE: employee_exits
-- Normalized exit log derived from termination_date +
-- termination_reason on the employees table.
-- Used by Cube.js attrition metrics.
-- ============================================================

CREATE TABLE hr.employee_exits (
    id              SERIAL PRIMARY KEY,
    employee_id     INT NOT NULL REFERENCES hr.employees(id),
    exit_date       DATE NOT NULL,
    exit_type       VARCHAR(20) NOT NULL,
    -- Values: voluntary | involuntary | retirement
    reason          VARCHAR(200),
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- SUPPORTING TABLE: performance_reviews
-- Two review cycles per employee per year.
-- ============================================================

CREATE TABLE hr.performance_reviews (
    id              SERIAL PRIMARY KEY,
    employee_id     INT NOT NULL REFERENCES hr.employees(id),
    review_date     DATE NOT NULL,
    rating          NUMERIC(3, 1) NOT NULL CHECK (rating BETWEEN 1.0 AND 5.0),
    reviewer_id     INT REFERENCES hr.employees(id),
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- SUPPORTING TABLE: hiring_requisitions
-- open/filled/cancelled job reqs per department.
-- days_open is NOT a generated column — CURRENT_DATE is not
-- immutable. Compute it in queries:
--   SELECT COALESCE(close_date, CURRENT_DATE) - open_date AS days_open
-- ============================================================

CREATE TABLE hr.hiring_requisitions (
    id              SERIAL PRIMARY KEY,
    department      VARCHAR(100) NOT NULL,
    open_date       DATE NOT NULL,
    close_date      DATE,
    status          VARCHAR(20) NOT NULL DEFAULT 'open',
    -- Values: open | filled | cancelled
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- APP TABLE: users
-- Auth accounts for the chatbot. employee_id links
-- a manager user to their team in the employees table.
-- ============================================================

CREATE TABLE hr.users (
    user_id         SERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    email           VARCHAR(150) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role            VARCHAR(20) NOT NULL CHECK (role IN ('analyst', 'manager', 'hr_admin')),
    employee_id     INT REFERENCES hr.employees(id),
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- APP TABLE: query_audit_log
-- Every /api/chat request is logged here regardless of outcome.
-- ============================================================

CREATE TABLE hr.query_audit_log (
    id              SERIAL PRIMARY KEY,
    user_id         INT REFERENCES hr.users(user_id),
    role            VARCHAR(20),
    query_text      TEXT,
    resolved_query  TEXT,
    metric_id       VARCHAR(100),
    execution_type  VARCHAR(20),
    -- Values: metric_route | llm_generated
    execution_ms    INT,
    cache_hit       BOOLEAN DEFAULT FALSE,
    session_id      VARCHAR(100),
    turn_number     INT,
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- APP TABLE: conversation_sessions
-- In-memory store is primary; this table persists sessions
-- for audit and resume-on-restart in v2.0.
-- ============================================================

CREATE TABLE hr.conversation_sessions (
    session_id      VARCHAR(100) PRIMARY KEY,
    user_id         INT REFERENCES hr.users(user_id),
    turns           JSONB DEFAULT '[]',
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- INDEXES
-- Covering the most frequent chatbot query patterns.
-- ============================================================

-- employees: department-level filtering (most common metric group-by)
CREATE INDEX idx_emp_dept_l1          ON hr.employees(department_l1);
CREATE INDEX idx_emp_dept_l2          ON hr.employees(department_l2);
CREATE INDEX idx_emp_status           ON hr.employees(employment_status);
CREATE INDEX idx_emp_level            ON hr.employees(level);
CREATE INDEX idx_emp_supervisor_id    ON hr.employees(supervisor_id);
CREATE INDEX idx_emp_start_date       ON hr.employees(start_date);
CREATE INDEX idx_emp_work_city        ON hr.employees(work_city);
CREATE INDEX idx_emp_work_mode        ON hr.employees(work_mode);
CREATE INDEX idx_emp_gender           ON hr.employees(gender);

-- exits: attrition queries by date range and type
CREATE INDEX idx_exits_employee_id    ON hr.employee_exits(employee_id);
CREATE INDEX idx_exits_exit_date      ON hr.employee_exits(exit_date);
CREATE INDEX idx_exits_exit_type      ON hr.employee_exits(exit_type);

-- performance: ratings aggregated by department/quarter
CREATE INDEX idx_reviews_employee_id  ON hr.performance_reviews(employee_id);
CREATE INDEX idx_reviews_review_date  ON hr.performance_reviews(review_date);

-- requisitions: open reqs by department
CREATE INDEX idx_reqs_department      ON hr.hiring_requisitions(department);
CREATE INDEX idx_reqs_status          ON hr.hiring_requisitions(status);

-- audit: user activity lookups
CREATE INDEX idx_audit_user_id        ON hr.query_audit_log(user_id);
CREATE INDEX idx_audit_created_at     ON hr.query_audit_log(created_at);
CREATE INDEX idx_audit_session_id     ON hr.query_audit_log(session_id);
