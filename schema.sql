CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    picture TEXT NOT NULL,
    price INTEGER NOT NULL,
    rate TEXT NOT NULL,
    country TEXT,
    departure TEXT
);