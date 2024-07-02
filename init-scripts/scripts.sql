-- init.sql

\c resumes_db;

CREATE TABLE IF NOT EXISTS main_data (
    id SERIAL PRIMARY KEY,
    resume_id text,
    url text,
    salary text,
    UNIQUE (resume_id)
);
