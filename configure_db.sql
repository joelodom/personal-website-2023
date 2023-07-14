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

