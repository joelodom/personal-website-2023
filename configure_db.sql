CREATE TABLE IF NOT EXISTS users (
    email VARCHAR(255) PRIMARY KEY,
    salt VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    session_secret VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS secrets (
    secret_key VARCHAR(255) PRIMARY KEY,
    secret_value VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS table_for_tests (
    some_key VARCHAR(255) PRIMARY KEY,
    some_value VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS user_sessions (
    session_id VARCHAR(255) PRIMARY KEY,
    principal VARCHAR(255) NOT NULL,
    expected_seq_num INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)