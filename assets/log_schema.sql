-- sudo su postgres
-- psql
CREATE DATABASE utilities OWNER csabimvp;

-- \q
-- psql -U csabimvp -d utilities
-- PROD schema
CREATE SCHEMA logs AUTHORIZATION csabimvp;

CREATE TABLE
    IF NOT EXISTS logs.dag_logs (
        data_items NUMERIC,
        description VARCHAR,
        finished TIMESTAMP,
        project_name VARCHAR,
        start TIMESTAMP,
        status_code NUMERIC,
        task_id VARCHAR PRIMARY KEY,
        task_name VARCHAR
    );