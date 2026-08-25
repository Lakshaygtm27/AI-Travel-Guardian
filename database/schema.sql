CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS destinations (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    country VARCHAR(100) NOT NULL,
    safety_score INTEGER,
    popularity_score INTEGER,
    avg_budget NUMERIC(12, 2)
);

CREATE TABLE IF NOT EXISTS trips (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(120) NOT NULL,
    source_city VARCHAR(120) NOT NULL,
    destination_city VARCHAR(120) NOT NULL,
    budget NUMERIC(12, 2) NOT NULL CHECK (budget >= 0),
    days INTEGER NOT NULL CHECK (days > 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS hotels (
    id SERIAL PRIMARY KEY,
    trip_id INTEGER NOT NULL REFERENCES trips(id) ON DELETE CASCADE,
    name VARCHAR(180) NOT NULL,
    city VARCHAR(120) NOT NULL,
    nightly_rate NUMERIC(12, 2) CHECK (nightly_rate >= 0)
);

CREATE TABLE IF NOT EXISTS attractions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(180) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL DEFAULT 'India',
    latitude FLOAT,
    longitude FLOAT,
    rating FLOAT,
    cost NUMERIC(12, 2)
);

CREATE TABLE IF NOT EXISTS expenses (
    id SERIAL PRIMARY KEY,
    trip_id INTEGER NOT NULL REFERENCES trips(id) ON DELETE CASCADE,
    category VARCHAR(80) NOT NULL,
    amount NUMERIC(12, 2) NOT NULL CHECK (amount >= 0),
    spent_at DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    trip_id INTEGER REFERENCES trips(id) ON DELETE CASCADE,
    title VARCHAR(180) NOT NULL,
    details TEXT,
    severity VARCHAR(20) NOT NULL DEFAULT 'info',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS weather_logs (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    temperature FLOAT NOT NULL,
    rain FLOAT NOT NULL,
    wind FLOAT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS risk_scores (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    risk_score INTEGER NOT NULL,
    risk_level VARCHAR(20) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS emergency_contacts (
    id SERIAL PRIMARY KEY,
    country VARCHAR(100) NOT NULL UNIQUE,
    police VARCHAR(30) NOT NULL,
    ambulance VARCHAR(30) NOT NULL,
    fire VARCHAR(30) NOT NULL,
    tourism VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS hospitals (
    id SERIAL PRIMARY KEY,
    name VARCHAR(180) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL DEFAULT 'India',
    latitude FLOAT,
    longitude FLOAT,
    phone VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS scams (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    scam VARCHAR(180) NOT NULL,
    severity VARCHAR(20) NOT NULL
);

CREATE INDEX IF NOT EXISTS trips_destination_city_idx ON trips(destination_city);
CREATE INDEX IF NOT EXISTS expenses_trip_id_idx ON expenses(trip_id);
CREATE INDEX IF NOT EXISTS alerts_trip_id_idx ON alerts(trip_id);