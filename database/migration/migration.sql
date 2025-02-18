CREATE TABLE IF NOT EXISTS weekly_plan (
    id TEXT PRIMARY KEY,
    category TEXT,
    activity TEXT,
    frequency TEXT,
    time TEXT
);

CREATE TABLE IF NOT EXISTS daily_schedule (
    id TEXT PRIMARY KEY,
    day INTEGER,
    activity_id INTEGER,
    completed INTEGER DEFAULT 0,
    FOREIGN KEY (activity_id) REFERENCES weekly_plan(id)
);
