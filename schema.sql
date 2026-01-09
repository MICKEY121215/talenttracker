CREATE TABLE Client (
    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE Role (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    title TEXT,
    jd_text TEXT,
    status TEXT,
    FOREIGN KEY (client_id) REFERENCES Client(client_id)
);
