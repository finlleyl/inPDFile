CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    full_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    jwt_token VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE pdf_documents (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    file_size INTEGER NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'в очереди',
    classification VARCHAR(50),
    metadata JSONB,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE pdf_processing_history (
    id SERIAL PRIMARY KEY,
    document_id INTEGER,
    status VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    log TEXT,
    FOREIGN KEY (document_id) REFERENCES pdf_documents(id)
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    task_id VARCHAR(255) NOT NULL,
    document_id INTEGER,
    status VARCHAR(50) DEFAULT 'выполняется',
    result TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (document_id) REFERENCES pdf_documents(id)
);
