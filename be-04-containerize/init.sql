CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Stretch goal: Add one index to optimize email lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

INSERT INTO users (name, email) VALUES 
('Ahmed Shahin', 'ahmed@example.com'),
('Test User', 'test@example.com') 
ON CONFLICT (email) DO NOTHING;
