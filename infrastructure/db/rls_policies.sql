-- ============================================================
-- HR Analytics Chatbot — Row Level Security Policies
-- File: infrastructure/db/rls_policies.sql
-- Run order: 02 (after schema.sql, before seed_data.sql)
-- ============================================================

-- ============================================================
-- ROLES
-- IF NOT EXISTS prevents crash if role already exists
-- (hr_admin is a built-in role in PostgreSQL 15)
-- ============================================================

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'hr_analyst') THEN
        CREATE ROLE hr_analyst;
    END IF;
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'hr_manager') THEN
        CREATE ROLE hr_manager;
    END IF;
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'hr_admin') THEN
        CREATE ROLE hr_admin;
    END IF;
END
$$;

-- ============================================================
-- ENABLE RLS ON SENSITIVE TABLES
-- ============================================================

ALTER TABLE hr.employees           ENABLE ROW LEVEL SECURITY;
ALTER TABLE hr.performance_reviews ENABLE ROW LEVEL SECURITY;

-- ============================================================
-- POLICIES: hr.employees
-- ============================================================

-- hr_admin sees all rows
CREATE POLICY admin_all_employees ON hr.employees
    FOR ALL
    USING (
        current_setting('app.user_role', true) = 'hr_admin'
    );

-- manager sees only their direct reports
CREATE POLICY manager_own_team ON hr.employees
    FOR SELECT
    USING (
        current_setting('app.user_role', true) = 'manager'
        AND supervisor_id = current_setting('app.user_id', true)::int
    );

-- analyst sees all active employees only
CREATE POLICY analyst_active_employees ON hr.employees
    FOR SELECT
    USING (
        current_setting('app.user_role', true) = 'analyst'
        AND employment_status = 'Active'
    );

-- ============================================================
-- POLICIES: hr.performance_reviews
-- ============================================================

-- hr_admin sees all reviews
CREATE POLICY admin_all_reviews ON hr.performance_reviews
    FOR ALL
    USING (
        current_setting('app.user_role', true) = 'hr_admin'
    );

-- manager sees reviews only for their direct reports
CREATE POLICY manager_team_reviews ON hr.performance_reviews
    FOR SELECT
    USING (
        current_setting('app.user_role', true) = 'manager'
        AND employee_id IN (
            SELECT id FROM hr.employees
            WHERE supervisor_id = current_setting('app.user_id', true)::int
        )
    );

-- analyst sees all reviews
CREATE POLICY analyst_all_reviews ON hr.performance_reviews
    FOR SELECT
    USING (
        current_setting('app.user_role', true) = 'analyst'
    );

-- ============================================================
-- GRANT PERMISSIONS
-- ============================================================

GRANT USAGE ON SCHEMA hr TO hr_analyst, hr_manager, hr_admin;

GRANT SELECT ON hr.employees           TO hr_analyst, hr_manager, hr_admin;
GRANT SELECT ON hr.employee_exits      TO hr_analyst, hr_manager, hr_admin;
GRANT SELECT ON hr.performance_reviews TO hr_analyst, hr_manager, hr_admin;
GRANT SELECT ON hr.hiring_requisitions TO hr_analyst, hr_manager, hr_admin;

GRANT ALL    ON hr.employees           TO hr_admin;
GRANT ALL    ON hr.employee_exits      TO hr_admin;
GRANT ALL    ON hr.performance_reviews TO hr_admin;
GRANT ALL    ON hr.hiring_requisitions TO hr_admin;
GRANT ALL    ON hr.users               TO hr_admin;
GRANT ALL    ON hr.query_audit_log     TO hr_admin;
GRANT ALL    ON hr.conversation_sessions TO hr_admin;

GRANT INSERT ON hr.query_audit_log       TO hr_analyst, hr_manager;
GRANT INSERT ON hr.conversation_sessions TO hr_analyst, hr_manager;

GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA hr TO hr_analyst, hr_manager, hr_admin;
